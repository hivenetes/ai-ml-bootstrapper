# Containerized RAG Pipeline

### Set Environment Variables

```bash
cp store_service/secret.example.txt store_service/secret.txt

# update the values
DO_SPACES_KEY=<update>
DO_SPACES_SECRET=<update> 
#save and exit the file
```

### Install Prerequisites
```bash
# Install needed tools and libraries from prerequisites.sh
./prerequisites.sh
```

### Run the application
```bash
# Spin up the containers
export NIVIDA_RUNTIME=true
./run.sh
```

![Alt text](./containerised-rag.png)