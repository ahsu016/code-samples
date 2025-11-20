# Word Graph React App

This is a React-based web application that visualizes word relationships such as synonyms, antonyms, and collocations using an interactive graph.

## Prerequisites

Before you begin, make sure you have the following installed on your machine: Node.js (version 14 or higher recommended) from https://nodejs.org/ and npm (comes with Node.js) or yarn (optional).

## Setup and Run Locally

1. Extract the project folder to your desired location.  
2. Open a terminal or command prompt and navigate into the project directory using `cd path/(WHERE THE PROJECT IS)`.  
3. Install dependencies by running `npm install` or `yarn`.  
4. Start the development server with `npm start` or `yarn start`. 
5. The app will open in your browser at `http://localhost:3000`. Enter a word, press Enter or click Search to see the interactive word relationship graph. Click nodes to fetch and view definitions.

## Build for Production

To create an optimized build for deployment, run `npm run build` or `yarn build`. The production-ready files will be generated inside the `build` folder.

## Notes

The app requires a backend API endpoint for fetching word data. Ensure the backend API URL is configured correctly in an environment file or in the code. Without a backend API (INCLUDED IN THE ZIPPED FILE), the app may not function correctly. Please make sure the backend API is included; if you preserve the contents of the .zip file in the file structure it is initially, it should work as intended.

## Troubleshooting

If you get errors about missing packages, make sure you ran `npm install` or `yarn`. If the app doesn’t start on port 3000, check that no other process is using that port or specify another port. Ensure Node.js and npm versions meet the prerequisites.

## Contact

For questions or help running this project, please contact me.