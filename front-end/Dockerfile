# Use the official Node.js image for building the React app
FROM node:18 as build

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the app
COPY . .

# Build the app
RUN npm run build

# Use a lightweight web server for serving the built app
FROM nginx:alpine

# Copy the built files to the Nginx HTML folder
COPY --from=build /app/build /usr/share/nginx/html

# Expose the port used by Nginx
EXPOSE 80

# Start the server
CMD ["nginx", "-g", "daemon off;"]