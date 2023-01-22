const cards = JSON.parse('{{ cards|tojson|safe }}');
let currentCardIndex = {{ current_card_index }};
let currentCard = cards[currentCardIndex];
let isFlipped = {{ flip }};

// Select the container element where the cards will be displayed
const cardsContainer = document.querySelector('.cards-container');

// Loop through the cardsData array
for (let i = 0; i < cardsData.length; i++) {
    // Create a new div element for each card
    let cardDiv = document.createElement('div');
    // Add a class to the div element for styling
    cardDiv.classList.add('card');
    // Set the card's rank and suit as the div's innerHTML
    cardDiv.innerHTML = `${cardsData[i].rank} of ${cardsData[i].suit}`;
    // Add the person, action and object to the card
    cardDiv.innerHTML += `<br> Person: ${cardsData[i].person} <br> Action: ${cardsData[i].action} <br> Object: ${cardsData[i].obj}`;
    // Append the card div to the container element
    cardsContainer.appendChild(cardDiv);
}

// Select the element with id "card-name"
const cardName = document.querySelector("#card-name");
// Set the text of the element to the current card's rank and suit
cardName.innerText = `${currentCard.rank} of ${currentCard.suit}`;

// Select the element with id "card-attributes"
const cardAttributes = document.querySelector("#card-attributes");

// Select the element with id "flip-button"
const flipButton = document.querySelector("#flip-button");

// Select the image element
const image = document.querySelector("#card-image");

// Add an event listener to the button that toggles the display of the card attributes
flipButton.addEventListener("click", () => {
    isFlipped = !isFlipped;
    cardAttributes.style.display = isFlipped ? "block" : "none";
    image.src = isFlipped ? "{{ url_for('static', filename='playing-cards/custom/' + current_card.img_path) }}" : "{{ url_for('static', filename='playing-cards/' + cards[currentCardIndex].img_path) }}";
});

// Select the element with id "next-button"
const nextButton = document.querySelector("#next-button");
// Add an event listener to the button that displays the next card in the cards array
nextButton.addEventListener("click", () => {
    currentCardIndex = (currentCardIndex + 1) % cards.length;
    currentCard = cards[currentCardIndex];
    cardName.innerText = `${currentCard.rank} of ${currentCard.suit}`;
    cardAttributes.innerHTML = `Person: ${currentCard.person}<br>
                                Action: ${currentCard.action}<br>
                                Object: ${currentCard.obj}`;
    image.src = "{{ url_for('static', filename='playing-cards/' + cards[currentCardIndex].img_path) }}";
});
