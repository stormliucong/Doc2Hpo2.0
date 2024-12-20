# Use the official Node.js image for building the React app
FROM node:18 as build

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the app
# not copy instead use Volume to mount the code from the host machine

# Start the React app
CMD ["npm", "start"]

