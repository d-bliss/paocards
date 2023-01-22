const cards = JSON.parse('{{ cards|tojson|safe }}');
let currentCardIndex = {{ current_card_index }};
let currentCard = cards[currentCardIndex];


});
