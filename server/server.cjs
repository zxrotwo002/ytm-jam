const http = require('http');

let currentCommand = null;

const server = http.createServer((req, res) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        res.writeHead(204);
        res.end();
        return;
    }

    if (req.method === 'POST' && req.url === '/command') {
        let body = '';
        req.on('data', chunk => { body += chunk.toString(); });
        req.on('end', () => {
            currentCommand = JSON.parse(body);
            console.log("External Command Received:", currentCommand);
            res.end("Queued");
        });
    } 
    else if (req.method === 'GET' && req.url === '/poll') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        if (currentCommand != null) {
            console.log("Sending " + currentCommand + " to Tampermonkey")
        }
        res.end(JSON.stringify(currentCommand));
        currentCommand = null; 
    }
});

server.listen(3000, () => console.log("Bridge Server active on port 3000"));