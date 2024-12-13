const express = require('express');
const app = express();
const port = process.env.PORT || 8080;

app.use(express.static('wwwroot'));

app.get('*', (req, res) => {
    res.sendFile('index.html', { root: 'wwwroot' });
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
