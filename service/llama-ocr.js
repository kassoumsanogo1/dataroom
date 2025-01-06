import { ocr } from 'llama-ocr';

async function runOCR(filePath) {
    if (!filePath) {
        console.error("Erreur : Aucun chemin d'image fourni.");
        process.exit(1); // Quitte le programme avec un code d'erreur
    }

    try {
        const markdown = await ocr({
            filePath: filePath, // Utilisation du chemin d'image passé en argument
            apiKey: process.env.TOGETHER_API_KEY
        });

        console.log(markdown); // Affiche le texte extrait
    } catch (error) {
        console.error("Erreur lors de l'extraction OCR :", error);
    }
}

// Récupération du chemin d'image depuis les arguments de la ligne de commande
const imagePath = process.argv[2]; // 3e élément du tableau `process.argv` (après "node" et le script)
runOCR(imagePath).catch(console.error);


// ocr.js
/* import { ocr } from 'llama-ocr';


async function runOCR() {
    const markdown = await ocr({
        //filePath: "https://github.com/user-attachments/assets/8138276f-a896-4c60-a8ca-4522054f06d4",
        filePath: "./trader-joes-receipt.png",
        //filePath: "mur.JPG",
        apiKey: process.env.TOGETHER_API_KEY
    });

    console.log(markdown);
}
//runOCR;
runOCR().catch(console.error); */
