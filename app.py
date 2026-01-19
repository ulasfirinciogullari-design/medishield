import streamlit as st
import boto3
import json

# GitHub Secrets'tan anahtarları çekiyoruz
aws_access_key = st.secrets["AWS_ACCESS_KEY_ID"]
aws_secret_key = st.secrets["AWS_SECRET_ACCESS_KEY"]

# Amazon Bedrock Bağlantısı
client = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1', # Senin Bedrock'ı açtığın bölge
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key
)

st.title("🛡️ ZAKShield AI")
st.write("Hukuki ve İdari Sağlık Asistanı")

prompt = st.text_input("Doktor, bugün sana nasıl yardımcı olabilirim?")

if prompt:
    # Bedrock Claude 3.5 Sonnet'i tetikliyoruz
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": prompt}]
    })
    
    response = client.invoke_model(body=body, modelId="anthropic.claude-3-5-sonnet-20240620-v1:0")
    response_body = json.loads(response.get('body').read())
    
    st.write("### ZAKShield Analizi:")
    st.write(response_body['content'][0]['text'])

