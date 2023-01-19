const cards = JSON.parse('{{ cards|tojson|safe }}');
let currentCardIndex = {{ current_card_index }};
let currentCard = cards[currentCardIndex];
let isFlipped = {{ flip }};

// Select the element with id "card-name"
const cardName = document.querySelector("#card-name");
// Set the text of the element to the current card's rank and suit
cardName.innerText = `${currentCard.rank} of ${currentCard.suit}`;

// Select the element with id "card-attributes"
const cardAttributes = document.querySelector("#card-attributes");

// Select the element with id "flip-button"
const flipButton = document.querySelector("#flip-button");
// Add an event listener to the button that toggles the display of the card attributes
flipButton.addEventListener("click", () => {
    isFlipped = !isFlipped;
    cardAttributes.style.display = isFlipped ? "block" : "none";
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
});
