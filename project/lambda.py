### 1st lambda function: serializeImageData
'''
event json:
{
  "key": "test/bike_s_000071.png",
  "bucket": "bmwsu"
}
'''
import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""
    
    # Get the s3 address from the Step Function event input
    # s3://bmwsu/test/bike_s_000071.png
    key = event['key']    ## TODO: fill in
    bucket = event['bucket']    ## TODO: fill in
    
    # Download the data from s3 to /tmp/image.png
    ## TODO: fill in
    s3.download_file(bucket, key, '/tmp/image.png')
    
    # We read the data from a file
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    # Pass the data back to the Step Function
    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }






### 2nd lambda function: classification
'''
event json:
{
  "inferences": [],
  "image_data": "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjUuMiwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy8qNh9FAAAACXBIWXMAAA9hAAAPYQGoP6dpAAAJ3UlEQVR4nEWUS28c13PFf3Xv7e55cTh8SBQlStaDsuwofgSOYwRBltnnc+QLJgiSbRaJYSOW5b8ty5ZkSyIpcTjDnp7p171VWVBACihUbQp1cOqckr78F9tUz7H+gs3mhGJ4naTK+z9fIJ2ji0bTg8uNj44fsr3zCaodm/YNWbZNlu/T15e0zRPW5ZKimFJkjvX5Je1K2H3wD8xufIpGiFoT+0uCG5CFGaYQkCXiLlDekfScZB4lYZQAqEJMMPCeLCuBc8AQWaLWogZGiXIBXELqEBG8Vjh1CJeYLDFJJKtIVHg3AecwEsHbEEkZ2gPR4VIOKJIcEj0SDReNnBGFHyMpw1uOtxEkh7cCswJJGZIynMtxSSAFJDk8Y7yNwVokbXAUCCMcI0AJkjyoYUlBDZIgIpDAImgULIKzDDGPqSEaQD1KREwQc0gSUIgKvYeIkMQhlkFySAJSBEAImHnMhKDWYtZhVJh2mK1RM1BDLRJ7wCD4BotrJKsxyXCuJ/VLxA4Q6TBrMOsxOswcQsJEkABGj1kDdGCGE0XoEQynKGYOtY4UFdUGTS2WBE1CjILDEVxPvSpR7VAXceIQXaMp4j4ARkHUyKKRRcGLR1yBmkMtgQpOPc4cogLJcBABI6mSEpgaKSkpGikampQsAydQLpf0dYlYd0Wj5iRtuAp3VSxidKhLSObxwQOKmWKaEARMUE2o9TijB1FMrxSvKmj6/wpCXnhAWJcNl+fnaF8Dgponaf3hrh4MQEmWSA7IciR4jIhZQjWCyAfACbMOZ9aDGWZXC80cKRqmQkqCCDhv1G2kb4TTVwtWywtEEomePlUfbHkFwBGuZhGy0Q4+G6AWSdqjFhGBlBS1hNHh1HrUEqqK6pXgrk6gxAjOB/I8EKNh0XH5ruH0zTu6rkKkJcb11ZDJByYykoIPI2a7dxHJMI2oRswiIkLsO2J/JVqHtVcMaCIlEEvQ9VgSUszJi4zxljAcgQToOuHibUW9rPBaU/Q9wSmI4NThnGEIo9E9xpOHmGU4NVz6oHpnWHoP3RwXE05TA6pYUkzlqo8JFIzIcJzwuRAGE+rkMGc0m45yWWKasNiBtDgfcU7wmcNnA4ajQ3AjDDCNWOpwIogzUr8ktQuIPSGlGqyDxNVSU2JSVI3gInk+ZtPusapGqNXM9jqavmFVBXZvXKOXFjMluITzgMvJioJ8MERpMTHUWmKs8XmBJSX2DaKBFFoCqcZZj0UwE8wMU8PMUB2yWNxmdXqD1YWR6kuC7zi4dQunOa9fbRhNN2yNhoiegDS4MCILW4gvSNKRTIGWZDVehqSux1mLFxBtCbGvCUQscfVS3Qc/C3Rpn+XFfVQeENenrOdLTpYlVXudu/eO+eXJr5xdvOef/+k+Nw/HiLRk+RZeRsQkJGs+OLPFaHESiH3CtCclxfkJoe9rfABT8O4qEcP5gDKmLAvMNlTvX7BZvGG+iPT9K7rOeH3S8fvrln/XV9y9XfL5303YyyasyxbvG/wARK5+hVlCcAgNsd1gVuAHLa6LDZ1EjAzvDSTigiPicKFmkp1C8y3qX9A5hRRpygvW5W84azi8PuW7H5f86785FucFeRjRbipSs0TiGt93iJYfSDVUS9pyhfhAnzaEru3IM8EMnPeAJ+SQDY29wxbVExbzmuc/R8r5kPsPPfW6ZHd2h2woxLOeTdWgOJq1gEWilljvyPuMSENKLY6Al0TTbFjXNVv7gWiRkDrFukgyJcuHZMWYQiMHRxnjMTi3YTwa8OR/Irkb8+Bhj5eOxdyxOj9jvai5sVvQbSqqy4b5ySkiBqGmrhbE2FAUgcxPQBtEjHyYI97hgsdpVLRLjMZDxttThqMdtravMd4egAW0LTh/U/Dmt8R61fDqtzmjPOdifsKbl++YFpHDazk3bxUs5xUvfnlDOS9wMqZendNUJX/82hLrAk1rhqOC2e4OLgvgHWE0HELq2d6Z4YsRSYUQJqg5qrVx8nvNT9+1WDLq9j1vX2RkmhgUhkuOe0eeiyrS9BC7RHWR+PGHilsP4dGjHu0c3/7Xe/pN4Oa9JeP9HbJBgYnhnBD2r1+jXnaUywGjKcACxzbOFTz9/g9+/VbI/IjPPxsxnCrP/9JQDDzDrYatQcT7DeWpgVd0lvPHc8/ZWcdwtGB94Fic5wSnvHm1QFU57ANZYUx2KohCaJrA81+MZz8v+frv93EOlu9bQtExygLWCYMd5dphx9FdYXsWGAyEqop88mjA9syxt6cMJw1bU+XsJHD3bsbR/oBUV+Q53P7IkDTih2/Pef3qDS6LfPOPY/KBEuZnHb8+XVGthPlZx+ZywNMf5tw5dvzVp0OOHlQ8+HjGzm7AZMGNI8/P/9sy2c4JuTEcCo++MMQrsYVHuwPGU+PH7zf87f6Y/RtLrh/mLN8nfn7akWfw8je4cZC4dU9xq2XFZ18MOLhVM9m6JPOR6VR4/HjKcNzz+TeJg6OG5XLDk+9bmjpRXmZc2ztkPm/IholPPx9x+6MZL58rdbtmtp/IMmW9Ao3KoIhMt0s+uhM4PITMGb/8WDM/rXGL+SXbsw3NOlGVl+xdq3n8BRT5hrM/E5OpJx/0dP2K8lKZbufcPTZG0w237gzJcs9kK2M8MfYP4NrBFnv7W3zypbJaNZz8PqBfBwZFzVdfb7Gz2/HpXwcs9qRWcdPxmBgDzXKLbjNg/7pw+w6sy5an3/esLoakJMz2jUefDnGu4c79RJJTjh9mDIrAT08uwG348puESM9i3nN4BPt7E14+67A4JMthNGkZjpW7x3D9usM5xQ0zEF8x3e05vDnDZT3PnyVWq4KjOwFrW6rLkswHdvegLZW+6tDaCG6Nk4bnTyOLkwFFLrx8UfLsLxe0K2M2XXPvIZyctBTFmNPTNYu55+1pxaryTGcZocgdFpXjRx3jSUW3cfzyY8uXX+3w+ItEU69YrwDXk1JDvYCu67l5a5c886wuS46PB6zLFk2Og5sD6mbFfNHhZU0oPN/9d2KyI8zfdazLCXc/HvHTpmRTDQkX78ecnbZ89jeG6gLtBzw8HrK91VKuSrrW8fZ1RjTj3oMZr84rLsseCYnNumNQZIjrqMqOsBgjI6Nu4HKpbG/lzGaeL74qaJuanZ1t+nbD9es5X32dk2Ut4T//4x1HN4b4FHC+x2cd+/uB0zcX9JrwruC3Zz0JwWeRqnFsbe/w/PeK5bLn4HBEte7AoG0aml4JHvLgaWvPcJhx97inXOQE77n/MTR1ye2jApWOMNsTHj12NGvFVhPI1qyrjlfPHCo5O4fK9t6ALsKfb1fs723RdQlzgeluzsuzmvXakWeetuuwHooQGA2VkDVUlePd2wznHCmr8d7zft6TB2H3wPF/3I0fv2K9VkoAAAAASUVORK5CYII="
}
'''
import json
import sagemaker
import base64
from sagemaker.serializers import IdentitySerializer

# Fill this in with the name of your deployed model
ENDPOINT = 'image-classification-2024-01-24-19-37-23-690'    ## TODO: fill in

def lambda_handler(event, context):

    # Decode the image data
    image = base64.b64decode(event['image_data'])    ## TODO: fill in)

    # Instantiate a Predictor
    predictor = sagemaker.predictor.Predictor(
        endpoint_name=ENDPOINT, 
    )    ## TODO: fill in

    # For this model the IdentitySerializer needs to be "image/png"
    predictor.serializer = IdentitySerializer("image/png")
    
    # Make a prediction:
    inferences = predictor.predict(image)    ## TODO: fill in
    
    # We return the data back to the Step Function    
    event["inferences"] = inferences.decode('utf-8')
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }






### 3rd lambda function filter low-confidence inferences
'''
event json:
{
  "inferences": [
    0.95,
    0.05
  ]
}
'''
import json


THRESHOLD = .93


def lambda_handler(event, context):
    
    # Grab the inferences from the event
    inferences = event['inferences']    ## TODO: fill in
    
    # Check if any values in our inferences are above THRESHOLD
    meets_threshold = 1 if max(inferences)>THRESHOLD else 0    ## TODO: fill in
    
    # If our threshold is met, pass our data back out of the
    # Step Function, else, end the Step Function with an error
    if meets_threshold:
        pass
    else:
        raise("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }