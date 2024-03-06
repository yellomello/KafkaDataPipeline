"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const app = (0, express_1.default)();
// Route to collect Gaussian whole number values
function generateGaussian(average, stdDev) {
    let u1, u2, z0;
    do {
        u1 = Math.random();
        u2 = Math.random();
        z0 = Math.sqrt(-2.0 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
    } while (isNaN(z0));
    return z0 * stdDev + average;
}
app.get("/api/gaussian/whole/:average/:std_dev", (req, res) => {
    const average = parseFloat(req.params.average);
    const stdDev = parseFloat(req.params.std_dev);
    // Generate Gaussian (normal) distribution values
    const data = Array.from({ length: 10 }, () => generateGaussian(average, stdDev));
    res.json({ values: data });
});
// Route to collect random fake names
app.get("/api/names", (req, res) => {
    // List of fake names (you can replace this with any data source)
    const fakeNames = [
        "John Doe",
        "Jane Smith",
        "Bob Johnson",
        "Evan Miller",
        "Vibek Dutta",
        "Alice Green",
        "James White",
        "Emily Brown",
        "Marc Thomas",
        "Mihir Rawat",
        "Noah Peters",
        "Sarah Lee",
        "William Davis",
        "David Johnson",
        "Oliver Wilson",
        "Zachary Nelson",
        "Natalie Martin",
        "Alexander Gray",
        "Alice Williams",
        "Charlie Browns",
        "Harleen Dhillon",
        "Charlotte Taylor",
    ];
    // Shuffle the names for randomness
    const shuffledNames = fakeNames[Math.floor(Math.random() * fakeNames.length)];
    res.json({ names: shuffledNames });
});
// Route to collect simple whole number data based on a 50/50 coin flip
app.get("/api/beta/whole/:probability_head/:probability_tail", (req, res) => {
    const probabilityHead = parseInt(req.params.probability_head) / 100;
    const probabilityTail = parseInt(req.params.probability_tail) / 100;
    // Generate whole number data based on a 50/50 coin flip
    const data = Array.from({ length: 10 }, () => Math.random() < probabilityTail ? 0 : 1);
    res.json({ values: data });
});
const port = 8100;
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
