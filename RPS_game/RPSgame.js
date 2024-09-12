const choices = ['rock', 'paper', 'scissors'];

const resultText = document.getElementById('result-text');
const userChoiceDisplay = document.getElementById('user-choice');
const computerChoiceDisplay = document.getElementById('computer-choice');

const choiceImages = document.querySelectorAll('.choice-img');

// see what the user chose
choiceImages.forEach(img => {
    img.addEventListener('click', (event) => {
        const userChoice = event.target.id;
        const computerChoice = getComputerChoice();
        const result = determineWinner(userChoice, computerChoice);

        // Display choices and result
        userChoiceDisplay.textContent = `You chose: ${userChoice}`;
        computerChoiceDisplay.textContent = `Computer chose: ${computerChoice}`;
        resultText.textContent = result;
    });
});

//generate random choice for the computer
function getComputerChoice() {
    const randomIndex = Math.floor(Math.random() * choices.length);
    return choices[randomIndex];
}

// determine the winner
function determineWinner(userChoice, computerChoice) {
    if (userChoice === computerChoice) {
        return "It's a tie!";
    } else if (
        (userChoice === 'rock' && computerChoice === 'scissors') ||
        (userChoice === 'paper' && computerChoice === 'rock') ||
        (userChoice === 'scissors' && computerChoice === 'paper')
    ) {
        return "You win!";
    } else {
        return "You lose!";
    }
}
