import json
import boto3

client = boto3.client(
    "sns",
    region_name="ap-southeast-1"
)

URL = "ALB-953733959.ap-southeast-1.elb.amazonaws.com"


def lambda_handler(event, context):
    # TODO implement
    if event["httpMethod"] == "POST":
        statusCode = 200
        try:
            information = json.loads(event["body"])
            phone_num = information["phone_number"]

            if "collected" in information:
                message = "successfully triggered - collection"
                client.publish(
                    PhoneNumber=f"+65{phone_num}",
                    Message="This message is to confirm that you have "
                            "successfully collected your item. Thank you")
            else:
                message = "successfully triggered - registration"
                ref = information["unique_ref"]
                location = information["location"]

                client.publish(
                    PhoneNumber=f"+65{phone_num}",
                    Message=f"Please collect your item at {location}, "
                            f"generate your QR code at this link: "
                            f"http://{URL}/api/qr/{ref} :)")

        except KeyError:
            return {
                'statusCode': 500,
                'body': json.dumps("Error occurred, wrong data")
            }
    else:
        statusCode = 405
        message = "Method not allowed"
    # return json.dumps("Hello")
    return {
        'statusCode': statusCode,
        'body': json.dumps(message)
    }

# def lambda_handler(event, context):
#     response = {
#         "statusCode": 200,
#         "body": json.dumps("Updated to new message")
#     }
#     return response
