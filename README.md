# Doc2Hpo2.0

Welcome to **Doc2Hpo2.0**, the upgraded version of the initial **Doc2Hpo**. This tool leverages new technologies and enhanced functionalities for Human Phenotype Ontology (HPO) term annotation and gene prioritization from free text. We hope you find **Doc2Hpo2.0** helpful for your projects! Contributions and feedback are welcome.


## Features

1. **New Tech Stack**: Built with a modern React front-end and Flask back-end.
2. **LLM Integration**: Includes large language model (LLM) capabilities for advanced text processing.
3. **Query and Annotate**: Query OARD to annotate the high or low frequency of HPO terms.
4. **Gene Prioritization**: Set priority for HPO terms to optimize gene prioritization algorithms.
5. **Organized Structure**: Separate `front-end` and `back-end` folders for a clean architecture.

---

## Repository Structure
- `front-end/`: React-based user interface.
- `back-end/`: Flask-based server-side logic.

---

## Prerequisites

Before setting up the project, ensure you have the following:

- Python 3.8+
- Node.js and npm
- OpenAI API Key (if you want to use GPT features)
- `hp.obo` file from the [HPO official website](https://hpo.jax.org/data/ontology)

---

## Setup Guide (Without Docker)

### Back-End Setup

1. **Navigate to the back-end folder:**
   ```bash
   cd back-end
   ```
2. **Install dependencies:**
   ```bash
   # Use virtual env if desired.
   pip install -r requirements.txt
   ```
   - Note: it can be difficult to install `nmslib` which is required by `scispacy`
3. **Add Required Files:**
   - Place your OpenAI API key in a file named `.api_key` in the `back-end` folder.
     ```bash
     echo "your_openai_api_key" > .api_key
     ```
   - Download `hp.obo` from the [HPO official website](https://hpo.jax.org/data/ontology) and place it in the `back-end` folder.

4. **Run the Flask server:**
   ```bash
   python app.py
   ```

### Front-End Setup

1. **Navigate to the front-end folder:**
   ```bash
   cd front-end
   ```
2. **Install dependencies:**
   ```bash
   npm install
   ```
3. **Start the development server:**
   ```bash
   npm start
   ```
4. **Access the application:**
   Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## Docker-Based Setup (Not recommended)

### Using Docker Compose

0. **THERE ARE BUGS WITH ARM64 KERNEL
   - This issue is due to dependency installation for Scispacy. Check [here](https://github.com/allenai/scispacy?tab=readme-ov-file#installation-note-nmslib)
   - This only works for a x86_64 machine.
   - As an alternative, try to build a X86_64 image for back-end
   ```sh
   cd backend
   docker build -t doc2hpov2.0-backend --platform linux/x86_64 .
   ```

1. **Ensure Docker and Docker Compose are installed:**
   - [Install Docker](https://docs.docker.com/get-docker/)
   - [Install Docker Compose](https://docs.docker.com/compose/install/)

2. **Place the required files in the back-end folder:**
   - `.api_key`: Contains your OpenAI API key.
   - `hp.obo`: Downloaded from the HPO website.

3. **Run the following command:**
   ```bash
   docker-compose up
   ```

4. **Access the application:**
   - Back-End API: [http://localhost:5000](http://localhost:5000)
   - Front-End App: [http://localhost:3000](http://localhost:3000)

---

## Testing Locally

To verify that the application is working:
1. Run the Flask server (back-end).
2. Run the React development server (front-end).
3. Use the browser to interact with the application at [http://localhost:3000](http://localhost:3000).
4. Verify API endpoints are functional by accessing [http://localhost:5000](http://localhost:5000).

---

## Deploy to Cloud (AWS or Other Vendors)

### AWS EC2 Deployment

1. **Set up an EC2 instance:**
   - Choose an instance type and OS (e.g., Ubuntu).
   - Configure security groups to allow ports 3000 and 5000.

2. **Install Dependencies:**
   - Python, Node.js, Docker (if using Docker setup).

3. **Transfer Files:**
   - Use `scp` or similar tools to upload your `front-end` and `back-end` folders.

4. **Run the Application:**
   - Follow either the non-Docker or Docker setup guide.

5. **Access the Application:**
   - Use the EC2 instance’s public IP address to access the app in your browser.

### Other Cloud Vendors

Follow the same deployment steps as AWS, adjusting for the specific platform’s requirements.

