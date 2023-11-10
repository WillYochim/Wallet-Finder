const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');

const app = express();
const port = 3000;

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

const dataFilePath = path.join(__dirname, 'portfolioData.txt');

// Read data from the file
function readDataFromFile() {
    try {
        const data = fs.readFileSync(dataFilePath, 'utf8');
        return JSON.parse(data);
    } catch (error) {
        return [];
    }
}

// Write data to the file
function writeDataToFile(data) {
    fs.writeFileSync(dataFilePath, JSON.stringify(data), 'utf8');
}

// Serve static files from the 'public' directory
app.use(express.static('public'));

// Endpoint for the root path
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Endpoint to get portfolio data
app.get('/api/portfolio', (req, res) => {
    const portfolioData = readDataFromFile();
    res.json(portfolioData);
});

// Endpoint to add an asset
app.post('/api/portfolio', (req, res) => {
    const newAsset = req.body;
    const portfolioData = readDataFromFile();
    portfolioData.push(newAsset);
    writeDataToFile(portfolioData);
    res.json(portfolioData);
});

// Endpoint to remove an asset
app.delete('/api/portfolio/:asset', (req, res) => {
    const assetToRemove = req.params.asset;
    const portfolioData = readDataFromFile();
    const updatedPortfolio = portfolioData.filter(asset => asset.asset !== assetToRemove);
    writeDataToFile(updatedPortfolio);
    res.json(updatedPortfolio);
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
