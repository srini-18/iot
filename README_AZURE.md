# Deploying to Azure Web App (Linux)

Quick steps to deploy this Flask + YOLO app to Azure App Service (Linux).

1. Ensure `requirements.txt` includes `gunicorn` (already added).

2. Create an App Service (example using Azure CLI):

```bash
az group create --name my-rg --location eastus
az appservice plan create --name my-plan --resource-group my-rg --is-linux --sku B1
az webapp create --resource-group my-rg --plan my-plan --name <YOUR_APP_NAME> --runtime "PYTHON|3.10"
```

3. Set the startup command (so Gunicorn serves the app):

```bash
# Option A: set startup command directly
az webapp config set --resource-group my-rg --name <YOUR_APP_NAME> --startup-file "gunicorn --bind=0.0.0.0:$PORT app:app"

# Option B: upload `startup.sh` and set it as startup file
az webapp deploy --resource-group my-rg --name <YOUR_APP_NAME> --src-path .
az webapp config set --resource-group my-rg --name <YOUR_APP_NAME> --startup-file "/home/site/wwwroot/startup.sh"
```

4. Deploy the code (example: ZIP deploy or `az webapp up`):

```bash
az webapp up --name <YOUR_APP_NAME> --resource-group my-rg --plan my-plan --sku B1
```

Notes:
- The app listens on the port provided by the environment variable `PORT` (fallback 8000).
- This project includes large ML dependencies; ensure the chosen App Service plan has enough memory/CPU.
- For production, consider using a GPU-enabled service or containerize the app and deploy to Azure Container Instances / AKS.
