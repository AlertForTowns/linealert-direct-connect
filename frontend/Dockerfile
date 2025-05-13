# Use an official Node.js runtime as the base image
FROM node:16

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to install dependencies
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the frontend code
COPY . .

# Build the frontend app for production
RUN npm run build

# Expose the port the app will run on
EXPOSE 3000

# Command to start the app
CMD ["npm", "start"]
