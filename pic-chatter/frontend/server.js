const express = require('express');
const path = require('path');
const fs = require('fs');
require('dotenv').config();
const multer = require('multer');
const { S3Client, PutObjectCommand } = require('@aws-sdk/client-s3');
const AWS = require('aws-sdk');
var gtts = require('node-gtts')('en');

const app = express();
const PORT = process.env.PORT || 3000;

// Ensure uploads directory exists
try {
    const uploadsDir = path.join(__dirname, 'uploads');
    if (!fs.existsSync(uploadsDir)){
        fs.mkdirSync(uploadsDir, { recursive: true });
        console.log('Created uploads directory');
    }
} catch (error) {
    console.warn('Warning: Could not create uploads directory:', error.message);
    // Continue execution as the application might not need uploads immediately
}

// Set EJS as the template engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Serve static files from uploads directory
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));

// Route to render the EJS template
app.get('/', (req, res) => {
    res.render('index', {
        apiEndpoint: process.env.API_ENDPOINT || 'https://default-endpoint.com',
        apiKey: process.env.API_KEY || 'default-api-key',
    });
});

app.get('/speech/:text', function(req, res) {
    res.set({'Content-Type': 'audio/mpeg'});
    gtts.stream(req.params.text).pipe(res);
})

// Health check endpoint
app.get('/health', (req, res) => {
    res.status(200).send('OK');
});

// Configure multer for file uploads
const upload = multer({ dest: 'PicChatter/' });

// Endpoint to handle image upload
app.post('/upload', upload.single('image'), async (req, res) => {
    try {
        if (!req.file) {
            console.error('No file uploaded');
            return res.status(400).json({ error: 'No file uploaded' });
        }

        console.log('Received file:', req.file);

        // Configure AWS SDK for DigitalOcean Spaces
        const spacesEndpoint = new AWS.Endpoint(process.env.SPACES_ENDPOINT);
        const s3 = new AWS.S3({
            endpoint: spacesEndpoint,
            accessKeyId: process.env.SPACES_KEY,
            secretAccessKey: process.env.SPACES_SECRET,
        });

        // Read the file content
        const fileContent = fs.readFileSync(req.file.path);

        // Prepare the upload parameters
        const params = {
            Bucket: process.env.SPACES_BUCKET,
            Key: req.file.originalname,
            Body: fileContent,
            ACL: 'public-read',
            ContentType: req.file.mimetype
        };

        // Upload to DigitalOcean Spaces
        const data = await s3.upload(params).promise();
        
        // Clean up the temporary file
        fs.unlinkSync(req.file.path);

        console.log('File uploaded successfully:', data.Location);
        res.json({ imageUrl: data.Location });

    } catch (error) {
        console.error('Error uploading file:', error);
        // Clean up the temporary file in case of error
        if (req.file && req.file.path) {
            fs.unlinkSync(req.file.path);
        }
        res.status(500).json({ error: 'Error uploading image' });
    }
});

// Start the server
const server = app.listen(PORT, '0.0.0.0', () => {
    console.log(`Server is running on port ${PORT}`);
});

// Handle graceful shutdown
process.on('SIGTERM', () => {
    console.log('SIGTERM signal received: closing HTTP server');
    server.close(() => {
        console.log('HTTP server closed');
        process.exit(0);
    });
});

process.on('SIGINT', () => {
    console.log('SIGINT signal received: closing HTTP server');
    server.close(() => {
        console.log('HTTP server closed');
        process.exit(0);
    });
});