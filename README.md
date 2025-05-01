# Personal-Budget-App

Deployment:
- there should be a link at the side: personal-budget-app-alpha.vercel.app
- that should take you to the deployed product

Running the App locally:
- if the deployment does not work it might be because of timing out due to the free plan the vender products offer
- to then run it locally you will need a .env file to be placed in the frontend/ directory
- the one line needed in that .env file is: VITE_API_URL=http://localhost:5001
- save that file then CD into backend/ and run "python main.py" 
- Then CD into frontend/ and run "npm run dev"