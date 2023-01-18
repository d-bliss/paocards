const cards = cardsData;
// Javascript that 
cards.forEach((card) => {
    const personInput = document.querySelector(
        `input[name='person_${card.std_card_id}']`
    );
    personInput.value = card.person;

    const actionInput = document.querySelector(
        `input[name='action_${card.std_card_id}']`
    );
    actionInput.value = card.action;

    const objInput = document.querySelector(
        `input[name='obj_${card.std_card_id}']`
    );
    objInput.value = card.obj;
});

