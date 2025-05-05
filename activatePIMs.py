import json
import random
import jwt
import uuid
import aiohttp
from azure.identity import DefaultAzureCredential
# from azure.mgmt.authorization import AuthorizationManagementClient
# from azure.identity import DefaultAzureCredential
import requests

# Initialize Azure credentials
cred = DefaultAzureCredential()
token = cred.get_token("https://management.core.windows.net/")

# List of PIM role names (same as in JS version)
pim_role_names = ["e24cc578-f8fb-466a-a8f3-0a9e451dc5cc",
    "a06cbad4-9a04-4403-8a64-1b616b46ea59",
    "3d9e23ba-25fc-4715-a44d-8b4806b2c220",
    "7af6fceb-caf1-4fd8-87c4-0e98e8bd9db1",
    "5bf2ad5e-86e3-43b3-8924-9590861ba704",
    "71ad213a-160e-4f59-8485-0dba1c856413",
    "b3f96541-7262-4d86-ba7e-a697d8ef492a",
    "3f9c33f4-12b0-4ad6-9bb3-9b91a3fd45c5",
    "a40d5ca1-8145-4d7e-821b-f71b88c4ad2f",
    "8aabc9d8-b4db-4df0-af9c-bc05b8ac6ad1",
    "62531528-f2dc-4d59-ad56-3c413f2c8b18",
    "29d45b0c-841d-477e-976e-e623b006d0ac",
    "ebfd6218-d272-4753-8d88-3b72cb5183cb",
    "3d6dfead-5224-4bc4-a289-cf101816af32",
    "10d89f9e-2143-4d47-8915-fd9f1b6943d8",
    "84b406e7-5d87-4c46-a332-c5a0b6f2e98d",
    "fa4979f8-15f1-4f6f-ae78-0f97b1bdc9ad",
    "6a5bcf69-3398-49e7-ab09-0edb6fb31c17",
    "abf28ba7-efb6-4fa0-aff6-32b566ee6eea",
    "90cc82ba-24f4-48b5-9ecf-7c75c79891ba",
    "3e9b40bf-61d0-45f5-8edb-cbf7a8fcb944",
    "d3afaa8b-03d3-4413-b4a9-20c1a860f95b",
    "fc2b0264-c35b-4733-8a20-cf97f66a062a",
    "a9e7fb5d-2cd4-4082-a3b5-67673981c2ad",
    "a07ac228-d4e6-47a0-ade7-ada7caf5541d",
    "5325f668-be55-4945-a9e2-797a72a6f709",
    "0d8bc04a-6640-43a6-910b-a6a7e3637fcd",
    "e0d6920e-2606-4650-9696-689bb28b4e8e",
    "a520669e-8880-4ac3-87be-069931b3abe0",
    "7132d878-a09c-47e9-be42-ef459df793f5",
    "e9c23c73-c816-4a08-864d-3964bdade42c",
    "4edd7062-924b-4e01-ba34-05b808008ace",
    "9a3cef89-6630-451b-90f4-a0faf1bff664",
    "3b85752a-74fe-4dde-9afc-6de46e5a4f16",
    "86a34bae-77d9-4cc6-bb31-b21d4ff94e2d",
    "5d5dab80-96a4-49c3-8372-4b459e4a8a86",
    "7d27f9e0-8ce2-4e00-b7a1-eb543b81b543",
    "17a931a5-9dee-4ab9-8147-110cec0086f5",
    "af2c891b-316d-4185-a8d0-98f7306b1395",
    "05ceb699-caae-4823-9638-176218c87397",
    "b55635ba-3519-4ce2-bcf3-6d0af958a1b4",
    "6c5e91ef-33bd-46c1-98c8-0014cc74160d",
    "d05282c8-1001-4753-8916-ed92b5880e6c",
    "3c8af1b4-820b-431e-8901-c2451ee28968",
    "d8be9e39-f0cf-4247-ac71-dd725d4d25d2",
    "6e5a4902-8e45-4af8-8627-90d87f50024a",
    "510cf4c9-f19b-4af0-90d4-594b918fa6eb",
    "0ae2a484-3f79-4810-b15e-2ef8588b8e48",
    "4c0788ee-0d46-42b1-8999-33e700328a2a",
    "e3c9a485-824f-4437-b44b-a90c394e6d0c",
    "c5078b1d-d32e-41f6-bcf5-6de4ca2674b4",
    "eb9c23d2-54a4-4cd5-a143-34964022f6ac",
    "d4d71cee-2215-4944-92f8-31471d61d77f",
    "e948d52e-c1d4-4c93-9d8a-0324f0c0d7af",
    "6f35d6d4-b454-46d9-b5f1-edb7cb5fcf66",
    "45b9e6d2-8775-48b8-9d7c-2cd185f806e7",
    "26b6179e-930a-459c-b257-553a43b2a5b7",
    "ee4e57ee-6bdb-40d1-b6fb-437053110bf4",
    "449bf8d7-11d9-4252-b821-58662678ee1c",
    "791ff6f7-7346-421c-b91b-7c8d0a99b921",
    "b7b37a10-5b58-4298-be2b-19bebdf40d84",
    "0b215909-0659-4d59-b9cc-45a8e7e30f17",
    "42071100-8441-4a59-806d-785a5152a120",
    "d1079516-ffbf-4f1f-95c3-66f9dbc60ed6",
    "98571ccf-c13e-4b09-b9e6-85326ed03963",
    "3e8ba4b8-8025-4e5b-ab74-d25e60648adf",
    "6436bf0c-5509-4657-9e18-ac344e700ecc",
    "f6adf107-7d47-46dd-8ca5-b290178913ad",
    "12adb0ce-c278-486c-b3f3-ea990adea20c",
    "8fb89ddf-88d6-4f4a-93cf-2f8f54d5c9c1",
    "305bf80c-2f86-4a56-82da-f99b13ab01d9",
    "751242e5-b50a-47c4-bf85-2815d99d3caf",
    "5ee43275-0793-4356-a1f3-64396297c8d5",
    "a92f9a5b-4eda-46a6-b0f1-32bb38d7c2fa",
    "4ec141c4-84fe-4db2-9d34-2f564f3e5e49",
    "083dae95-a40c-4acd-9fba-93c5225dcb3d",
    "3f3eca14-4b41-4317-b9f8-ccc418f4730b",
    "874686e3-6e0e-452a-8274-b1e9576b13f1",
    "5231846c-04d3-4b56-8aab-1ec8380d7542",
    "7a0501fa-3df9-4eff-9ed3-482246c1c83d",
    "000f1e64-4dd3-45a2-a4e1-2f3f3ae9f952",
    "51f9f5e9-c27b-4d1c-ba2a-481bffbc51df",
    "bc0c7a16-264f-40c5-8d1d-72f09b1d89ac",
    "b5e31d7f-4e58-4b4a-9dc4-f9e502f809f2",
    "fa3778cc-a8f8-41f4-bf3f-571cce3a20bb",
    "cdd2c063-4b49-476b-b2d5-f1d58d74be69",
    "ca7b0514-011a-4894-bc56-bc0a2535cfe3",
    "2ec4901c-5a77-41e3-87ef-048100d9e432",
    "f819ebb6-6ee0-4060-b45d-96b466c23da4",
    "dfaf47e7-5a42-4955-84a0-5df52f4cd2f9",
    "9e08f822-af75-46dd-88c9-1c0847c82fe5",
    "5194386b-5ba7-4ebe-818c-224c54693265",
    "1225ae3f-9527-4505-a8fb-9f3c4c7a90e9",
    "41075be9-e282-4f3f-8712-66649bf01b68",
    "a0801198-3f8d-4cd8-8e29-6689cc2adca7",
    "32cd9488-e522-4dd2-a141-9543ad64867d",
    "999d1a38-507f-41c3-840f-1338cf45d0a7",
    "49bc6c8e-fa0e-4967-8a4c-3b68d96f15fb",
    "df28052b-f517-4d24-ba5a-d1714370cffe",
    "2dfd54de-c2ca-4464-abc3-7c296feaa541",
    "33da7552-886c-4701-99ec-14fc32330c94",
    "94b2aeaa-a86f-4df9-9ee1-8d90df5edc61",
    "87100af8-8405-4ffd-b07f-d8e308a4dfaf",
    "5b6377c4-bb7c-4e24-9aa3-130b7826bf60",
    "95a0c2fd-c819-497f-86f5-503f29ba5e05",
    "dfae69bf-75c8-443d-bdc5-00f176b109c1",
    "56a3d1eb-9def-44e3-8c7d-783e4aa0bac9",
    "5839ef23-97e9-4861-b495-6dad0a813448",
    "bbc42917-cd7a-4b81-8c1d-f857bb48f201",
    "f8e994e5-f8e2-4032-902f-10b068c176c5",
    "ca3ef4ee-02d4-49fd-8384-c871e595db76",
    "3a3bbe2f-cbba-4341-bf70-e303f3145ea9",
    "fd602a7e-bd15-4455-94de-76563e0cd591",
    "b12d65cb-cf67-4559-a36e-afb583b0eeea",
    "03661d6f-ad8d-430e-864a-5eeb0d466a1d",
    "1e406fb9-1754-435f-b54e-b43d36c047f1",
    "25f9805e-e84b-48b7-b151-8e3c518d1f85",
    "1ef5fed3-e359-4fad-ae26-32a401127594",
    "56dffef7-8490-4ff5-8440-f3af3b52a2a3",
    "45eba57d-a25b-4cb0-946e-1dd6960419f2",
    "4f707423-ad2b-417d-ba6a-99c787c4b809",
    "19c717f1-16c4-4e3d-aabc-66223bd5a4c6",
    "211afc31-e175-49e3-85fd-d985c63e0503",
    "ed94a7d0-25f5-47f5-9b97-b057d0dffb81",
    "dda98cab-cf15-486d-b7bf-11bb93b8d768",
    "f9201d78-098b-4084-ae25-db6bd2c324e3",
    "90e0921d-66ac-4834-8d33-6e2f6ee1ae13",
    "d16c5277-2edd-4b29-9b47-e6b80d9e43e2",
    "e9cff804-f8a9-421d-badc-acba2e06657c",
    "fb6778b0-3fbc-480f-ba8c-eb1a765b3801",
    "d87b2f41-ee75-4e59-a6a8-6854c5f32be7",
    "5b28ebc7-9d57-45ad-9125-1b55e072f576",
    "b75722ef-ad7e-430a-ab69-9ef7b967c37d",
    "229a910f-ba92-4fc3-b367-5c0d3ba1b1cc",
    "bd425f30-2707-46b4-b307-370d22a80bcd",
    "b2281cf2-11a3-4e62-b8aa-51ff600b0c82",
    "e302b868-3351-47e7-a030-a2456fccbdc8",
    "04e5dfaa-a2ca-4dff-a4d3-11197156665a",
    "c41f080d-36c0-4386-91e0-5100237eeff4",
    "8c48fffe-ff2e-42bf-891d-0afc04be8eee",
    "a395c081-c742-46fe-9663-af78dda7764d",
    "dfc9c5bb-2bc4-4524-9f40-063f90bcfb07",
    "ee8ddaad-b3e6-461a-92a8-1e634d40dac2",
    "5723283f-8e8e-4589-9824-468790a09ff0",
    "c2cba9bd-3649-45c8-ab1d-5799f6ddd34e",
    "3fd0a061-f99c-4027-8c50-2dcedaa302f3",
    "551dc495-94b4-46d8-b899-1897ae277b41",
    "2e1842db-7c21-4889-95ad-c0c72de0f6eb",
    "dfe3fd3b-8444-4da0-83f3-164027a9d976",
    "002369c8-a4bc-44d3-9f69-0f7875ad0817",
    "7d5361ab-2c17-4089-a22a-37bf27a3d1e0",
    "e2fbcba1-e6a9-4712-8a82-dc1bb14c06b4",
    "cc83eda6-b6ad-4545-b440-08df528c1e0d",
    "b3799b15-cceb-478d-84f1-ab419fc77f9c",
    "ae3627c3-a779-4a2b-9f28-dc9d3c362b5d",
    "96209a91-6eaf-4e98-98fc-8d5f78705c91",
    "06fb7fea-29dd-42ee-8fe8-59edbd18fa02",
    "4af81ab0-7992-4887-813f-d3244d90f23e",
    "3087292b-3723-4a5f-9130-b56bd6a7c73d",
    "1c2cda41-bc85-4b69-b9f7-5ca6ea8bed16",
    "cfd295ab-053e-4baa-b0e7-7abe0cf8b779",
    "74cfd643-a55e-42fa-a5b4-961fc772993b",
    "5f3b0c4d-1e05-4321-9fac-2e791299b567",
    "00b5cb31-7bc9-45ff-885f-4656577d2ef4",
    "736516e2-c080-4b79-be34-8ccb79259882",
    "e264bdbe-f001-47fd-8292-b4e1c24a9add",
    "f9a6fdfd-0933-4fb2-bb22-97a33d52e157",
    "c0d6f826-f027-4c28-8389-b5d2ba267657",
    "715d839a-491a-4259-b9d1-7c0bd794f89b",
    "d282da29-6734-455d-854e-2ba44be2c6ab",
    "5e86cddd-51f4-435c-855e-eb81f9116f23",
    "b7da16f6-e683-46cb-a8d0-34c629291cbb",
    "753be71f-9c55-4f1f-99bf-909e7f6d7439",
    "fb650b2e-2496-4812-b7c2-4856ad27b634",
    "945cf871-90f3-40c2-9ac8-9c7f97b75729",
    "4618d67f-3391-495c-a7f1-d65fa5f1b41c",
    "d9a7a3ad-8f5b-480c-80ca-1c98ad800ef0",
    "8dd08607-2ee8-495d-8750-178cece471e1",
    "7fab03b8-7772-4eae-a4e0-454d8c71b44f",
    "81399273-ad92-4c76-8b22-43b884d45955",
    "31de30b8-864f-45dc-bce9-ede783f2e293",
    "bf0da4a8-4ff3-4669-aa0d-a780ab6b34ae",
    "86d891b7-d060-42b2-87a3-16afe352d7da",
    "bf40b20a-1b08-416f-8f34-8ebf66b9b4d7",
    "43abb24d-4e0e-4f19-b384-3bda3203a82d",
    "e64a66a9-4e3c-47b6-a728-d1dc25e11c59",
    "c9d6b228-c01d-4c25-9c94-4bb184d6f149",
    "22c0115d-d3b3-40cc-b59f-4e2e35ecbddc",
    "7589375c-686a-4c4a-bb27-6097d915cc3b",
    "c44d2df6-7459-4e57-91c5-aabc7d1483ee",
    "b68c9a39-b8ae-4007-8f8e-eb09387e2da5",
    "ce3a587a-470f-446d-80a6-a9ad868f5111",
    "36ef8e50-6e5c-4510-ba63-40b699e95c9b",
    "2e97a0e9-81c4-4939-9222-054352005dbf",
    "3dbd93bc-c0b6-46b7-a794-32b20e28d715",
    "5d0173e9-8dee-4a2d-b2ff-e1001b0c5d88",
    "6d36619c-ca4f-4ed2-91cf-f4cc7a4a3c8f",
    "3d2597ab-a06a-468f-adee-981df09d834c",
    "a7ae4e4f-35d9-4bf2-bdc0-9d4a63ca8216",
    "3135ff78-d57f-4aca-90d0-d3ef84d927c9",
    "94f3a175-fdb3-4cf8-801b-4a24ec9362f5",
    "6765df54-e4ce-42a9-91b2-87bd6c25a4be",
    "9c7085d4-b56e-476a-80c4-41d55c7416d9",
    "17a9cf7a-6fd1-449f-ad9c-d43c88548820",
    "51bcecd8-9772-4ae0-9d02-fafe2c1fdfad",
    "9b6fb7c8-c6bd-41fc-a5da-f7afc6b2b4f5",
    "860083e3-05d2-4b85-a831-70c756f41e66",
    "68933e89-c971-48d7-ac50-85cea366bb85",
    "a8017ee0-7c1a-4b65-8a46-fcfbd2348835",
    "83f8395a-c323-4e18-a41f-9da886cde29e",
    "73da9c87-ed55-4698-b929-4f67632b4624",
    "2b53fea3-aaf9-4d60-9e0e-453bbe8efc4a",
    "9022c3b1-f086-40ce-9f2f-527ba7812bcb",
    "229bb06e-0049-41e6-82ab-8c86b2593e9f",
    "48a39417-4f2b-4077-82e5-ff327a842892",
    "7b1b7883-40c0-4f01-83f2-c14906124724",
    "96b8acec-b21c-49b9-89a1-df90eec6d305",
    "9ad40eaf-c2ef-4ad9-a242-0d9ba388e518",
    "4968fa89-7710-45bb-a495-6f9511dfd596",
    "0d8ebbea-c3cb-45e8-85b8-6e2bb8d44a78",
    "a2b54cd9-54e4-4d8d-9a8b-6e885a4fc498",
    "2fb4e16e-68b6-49b2-af53-9d303608afe2",
    "29e43b6a-d306-471f-9abf-637de882aafa",
    "b9855f80-b83a-4be8-8f2a-58774ee8bf6f",
    "116f38a9-94f5-4699-838c-4bc3fd7ecc9b",
    "ecd874b8-9f94-49c3-b23f-64fc13ff09dc",
    "b48ca47a-11d4-40dd-96ef-4abd093a65b8",
    "a0effb26-d9ee-4749-96d7-b3e4c26d7509",
    "6d96e646-4760-48af-9b95-4733c0393efb",
    "7da1f70c-2e03-4b21-866e-799ca01510ed",
    "3a0ffbb9-7cb1-450a-b74e-ac4b49524dad",
    "6dd751ad-88c5-44a6-bb46-4eed5d9c5353",
    "d8cc9c63-fa2c-4b6e-93b9-8f265d76be11",
    "03a05e33-7210-4289-82b6-5460e206ffec",
    "25008612-7e92-4df5-8758-8135c3bd2370",
    "d82d4f28-39ff-4666-bc71-aa4b51881d96",
    "adeb190b-f981-4cfa-a9e1-9b8ab22fac6c",
    "139cb515-c13c-4f77-9472-49658ed6968d",
    "273ea2c4-fb41-4140-990e-28ee16187994",
    "e8d499b3-edcf-4fef-9173-87701daaea43",
    "a6bd3bca-ec25-4446-98ab-1de5dd1ae7f3",
    "19cf41c1-a93e-4b6d-bff7-2ac6402b2e67",
    "b2e2b115-86cd-476f-a5d7-044857cbd47d",
    "7298e866-d501-4240-9576-4d3363be3e0f",
    "58c30513-0c20-4fee-8879-661c6b0ceac4",
    "ab99c525-10fa-4d05-9158-ec8c35cb87fd",
    "90d42eb3-8858-42fa-b501-c1fc569929d1",
    "de1d0bf6-ebbb-40ec-b264-541f4c5ba823"]

def parse_oid_from_token(token_str):
    try:
        decoded = jwt.decode(token_str, options={"verify_signature": False})
        if isinstance(decoded, dict) and "oid" in decoded:
            # print("Decoded token:", decoded)
            return decoded["oid"]
        return ""
    except Exception as error:
        print("Failed to decode token:", error)
        return ""

# print("getting token:", token.token)
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
        pim_roles = [role for role in response.json()['value'] if role['properties']['roleEligibilityScheduleId'].split('/')[-1] in pim_role_names]
        print("Rertrieved roles")
        return pim_roles
    except Exception as error:
        print("Error fetching available roles:", error)
        return []

def get_request_body(pim_role):
    if not user_oid:
        print("User OID is not set.")
        return {}
    
    return {
        "Properties": {
            "PrincipalId": user_oid,
            "RoleDefinitionId": pim_role["properties"]["roleDefinitionId"],
            "RequestType": "SelfActivate",
            "LinkedRoleEligibilityScheduleId": pim_role["properties"]["roleEligibilityScheduleId"],
            "Justification": "developer accessing resources",
            "ScheduleInfo": {
                "StartDateTime": None,
                "Expiration": {
                    "Duration": "PT480M",
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

def export_role_assignments_to_csv(scope='/', csv_filepath='RoleDetails.csv'):
        try:
            # Get Azure credentials
            credential = DefaultAzureCredential()
            
            # Initialize the Authorization client
            auth_client = AuthorizationManagementClient(credential, subscription_id)
            
            # Get role assignments
            results = auth_client.role_eligibility_schedules.list(scope=scope, filter="asTarget()")
            print(f"Total roles fetched: {len(list(results))}")
            
            # Create output directory if it doesn't exist
            directory_path = os.path.dirname(csv_filepath)
            if directory_path and not os.path.exists(directory_path):
                os.makedirs(directory_path)
            
            # Process and write to CSV
            with open(csv_filepath, 'w', newline='') as csvfile:
                fieldnames = ['RoleName', 'Resource', 'ResourceType', 'Role_Guid', 
                            'SubscriptionID', 'Reason', 'Activate']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for role in results:
                    # Extract subscription ID from the role.id
                    subscription_id = role.id.split('/')[2] if role.id else ''
                    
                    writer.writerow({
                        'RoleName': role.role_definition_display_name,
                        'Resource': role.scope_display_name,
                        'ResourceType': role.scope_type,
                        'Role_Guid': role.name,
                        'SubscriptionID': subscription_id,
                        'Reason': 'dev',
                        'Activate': True
                    })
            
            print(f"CSV file created at: {csv_filepath}")
            
        except Exception as e:
            print(f"Error: {str(e)}")
            raise
def get_role_guids():
        try:
            # Read the CSV file
            df = pd.read_csv(r"C:\Users\smandadi\OneDrive - Microsoft\Desktop\sublime_stuff\PIM Activations\RoleDetails.csv")
            # Extract Role_Guid column as a list of strings
            role_guids = df['Role_Guid'].astype(str).tolist()
            
            return role_guids
        except FileNotFoundError:
            print("Error: RoleDetails.csv file not found")
            return []
        except KeyError:
            print("Error: Role_Guid column not found in the CSV file")
            return []

# roles = export_role_assignments_to_csv(scope='/', csv_filepath='RoleDetails.csv')
# if(roles is None):
#    roles = get_role_guids()

#  async def activate_pim_roles():
#     pim_roles = await get_available_roles()
#     async def activate_role(pim_role):
#         url = get_url(pim_role["properties"]["roleEligibilityScheduleId"])
#         request_body = get_request_body(pim_role)
#         max_retries = 5
#         base_delay = 2  # Base delay in seconds
#         try:
#             print("Activating role: " + pim_role["properties"]["expandedProperties"]["roleDefinition"]["displayName"] +
#                   " for " + pim_role["properties"]["expandedProperties"]["scope"]["displayName"])
#             async with aiohttp.ClientSession() as session:
#                 async with session.put(url, headers=create_headers(), json=request_body) as response:
#                     if response.status <= 299:
#                         print("Role activated successfully : "+ pim_role["properties"]["expandedProperties"]["roleDefinition"]["displayName"] +
#                   " for " + pim_role["properties"]["expandedProperties"]["scope"]["displayName"])
#                     # if response.status == 429:
#                     #     # Get retry-after header or use default delay
#                     #     retry_after = int(response.headers.get('Retry-After', base_delay))
#                     #     # Add jitter to prevent synchronized retries
#                     #     jitter = random.uniform(0, 1)
#                     #     delay = (base_delay * (2 ** attempt) + jitter) if retry_after <= base_delay else retry_after
#                     #     print(f"Rate limited. Waiting {delay:.2f} seconds before retry...")
#                     #     await asyncio.sleep(delay)
#                     #     # continue
#                     if response.status == 400:
#                         if response.text().contains("Role assignment already exists"):
#                             print("Role assignment already exists.")
#                     if response.status >= 300:
#                         raise Exception(f"HTTP {response.status}: {await response.text()}")
#             response.raise_for_status()
#         except Exception as error:
#             print("Error activating role:", getattr(error.response, 'status_code', None))
#             print("Error details:", getattr(error.response, 'text', str(error)))

#     await asyncio.gather(*(activate_role(pim_role) for pim_role in pim_roles))

async def activate_pim_roles():
    pim_roles = await get_available_roles()
    
    async def activate_role(pim_role):
        url = get_url(pim_role["properties"]["roleEligibilityScheduleId"])
        request_body = get_request_body(pim_role)
        max_retries = 5
        base_delay = 2  # Base delay in seconds
        
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
                if attempt == max_retries - 1:  # Last attempt
                    print(f"Final error activating role after {max_retries} attempts: {error}")
                else:
                    delay = base_delay * (2 ** attempt)
                    print(f"Error on attempt {attempt + 1}, retrying in {delay} seconds...")
                    await asyncio.sleep(delay)
                    continue

    # Process roles sequentially with delay
    batch_size = 10
    for i in range(0, len(pim_roles), batch_size):
        batch = pim_roles[i:i + batch_size]
        await asyncio.gather(*(activate_role(role) for role in batch))
        # Small delay between batches to prevent rate limiting
        await asyncio.sleep(1)

if __name__ == "__main__":
    import asyncio
    asyncio.run(activate_pim_roles())