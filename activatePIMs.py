import argparse
import json
import jwt
import uuid
import aiohttp
from azure.identity import DefaultAzureCredential
import requests

# Initialize Azure credentials
cred = DefaultAzureCredential()
token = cred.get_token("https://management.core.windows.net/")

def parse_oid_from_token(token_str):
    try:
        decoded = jwt.decode(token_str, options={"verify_signature": False})
        if isinstance(decoded, dict) and "oid" in decoded:
            return decoded["oid"]
        return ""
    except Exception as error:
        print("Failed to decode token:", error)
        return ""

user_oid = parse_oid_from_token(token.token)

def create_headers():
    return {
        "Authorization": f"Bearer {token.token}",
        "Content-Type": "application/json"
    }

def generate_guid():
    return str(uuid.uuid4())

def get_url(subscription_with_resource):
    role_assignment_request = subscription_with_resource.replace("roleEligibilitySchedules", "roleAssignmentScheduleRequests")
    role_assignment_request = role_assignment_request[:role_assignment_request.rindex('/')]
    role_assignment_request = f"{role_assignment_request}/{generate_guid()}"
    return f"https://management.azure.com{role_assignment_request}?api-version=2020-10-01"

async def get_available_roles():
    url = 'https://management.azure.com/providers/Microsoft.Authorization/roleEligibilityScheduleInstances?api-version=2020-10-01&$filter=asTarget()'
    try:
        print("Fetching available roles...")
        response = requests.get(url, headers=create_headers())
        pim_roles = response.json()['value']
        print("Retrieved roles")
        return pim_roles
    except Exception as error:
        print("Error fetching available roles:", error)
        return []

def get_request_body(pim_role, justification, duration):
    if not user_oid:
        print("User OID is not set.")
        return {}
    
    return {
        "Properties": {
            "PrincipalId": user_oid,
            "RoleDefinitionId": pim_role["properties"]["roleDefinitionId"],
            "RequestType": "SelfActivate",
            "LinkedRoleEligibilityScheduleId": pim_role["properties"]["roleEligibilityScheduleId"],
            "Justification": justification,
            "ScheduleInfo": {
                "StartDateTime": None,
                "Expiration": {
                    "Duration": f"PT{duration}M",
                    "Type": "AfterDuration"
                }
            },
            "TicketInfo": {
                "TicketNumber": "",
                "TicketSystem": ""
            },
            "IsActivation": True,
            "IsValidationOnly": False,
        }
    }

async def activate_pim_roles(batch_size=10, justification="developer accessing resources", duration=480):
    pim_roles = await get_available_roles()
    
    async def activate_role(pim_role):
        url = get_url(pim_role["properties"]["roleEligibilityScheduleId"])
        request_body = get_request_body(pim_role, justification, duration)
        max_retries = 5
        base_delay = 2
        
        for attempt in range(max_retries):
            try:
                role_name = pim_role["properties"]["expandedProperties"]["roleDefinition"]["displayName"]
                scope_name = pim_role["properties"]["expandedProperties"]["scope"]["displayName"]
                print(f"Activating role: {role_name} for {scope_name}")
                
                async with aiohttp.ClientSession() as session:
                    async with session.put(url, headers=create_headers(), json=request_body) as response:
                        if response.status <= 299:
                            print(f"Role activated successfully: {role_name} for {scope_name}")
                            return
                        
                        if response.status == 429:
                            retry_after = int(response.headers.get('Retry-After', base_delay))
                            delay = max(base_delay, retry_after)
                            print(f"{role_name} for {scope_name} Rate limited. Waiting {delay} seconds before retry...")
                            await asyncio.sleep(delay)
                            continue
                            
                        if response.status == 400:
                            text = await response.text()
                            if "Role assignment already exists" in text:
                                print(f"Role assignment already exists : {role_name} for {scope_name}.")
                                return
                            
                        if response.status >= 300:
                            raise Exception(f"HTTP {response.status}: {await response.text()}")
                
            except Exception as error:
                if attempt == max_retries - 1:
                    print(f"Final error activating role after {max_retries} attempts: {error}")
                else:
                    delay = base_delay * (2 ** attempt)
                    print(f"Error on attempt {attempt + 1}, retrying in {delay} seconds...")
                    await asyncio.sleep(delay)
                    continue

    # Process roles in parallel batches of 10
    batch_size = 10
    for i in range(0, len(pim_roles), batch_size):
        batch = pim_roles[i:i + batch_size]
        await asyncio.gather(*(activate_role(role) for role in batch))
        await asyncio.sleep(1)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Activate PIM roles in parallel')
    parser.add_argument('-b', '--batch-size', 
                       type=int, 
                       default=10,
                       help='Number of roles to activate in parallel (default: 10)')
    parser.add_argument('-j', '--justification',
                       type=str,
                       default="developer accessing resources",
                       help='Justification for role activation')
    parser.add_argument('-d', '--duration',
                       type=int,
                       default=480,
                       help='Duration in minutes for role activation (default: 480)')
    return parser.parse_args()


if __name__ == "__main__":
    import asyncio
    args = parse_arguments()
    asyncio.run(activate_pim_roles(
        batch_size=args.batch_size,
        justification=args.justification,
        duration=args.duration
    ))