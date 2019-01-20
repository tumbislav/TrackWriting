/*
writing.js
@author: Marko Čibej
@description: javascript for the front-end.
*/

function loadCards(data) {
  let deck = $('#full-deck');
  let card_template = $($('#card-template').html());
  let sep2 = $($('#card-sep-2').html());
  let sep3 = $($('#card-sep-3').html());
  let sep4 = $($('#card-sep-4').html());
  let sep5 = $($('#card-sep-5').html());

  for (let [row, card_data] of data.entries()) {
    let newCard = card_template.clone();
    newCard.find('#work-title').html(card_data.name);
    newCard.find('#count-top').html(card_data.word_count);
    newCard.find('#world').html(card_data.world);
    newCard.find('#series').html(card_data.series);
    newCard.find('#genre').html(card_data.genre);
    newCard.find('#type').html(card_data.type);
    newCard.find('#status').html(card_data.status);
    newCard.find('#count').html(card_data.word_count);
    deck.append(newCard);

    if (row % 2 == 1) { deck.append(sep2.clone()); }
    if (row % 3 == 2) { deck.append(sep3.clone()); }
    if (row % 4 == 3) { deck.append(sep4.clone()); }
    if (row % 5 == 4) { deck.append(sep5.clone()); }
  }
}

$(document).ready(function() {
  $.ajax({
    type: 'GET',
    url: '/cards',
    contentType: 'application/json; charset=utf-8',
    dataType: 'json',
    success: function(a){loadCards(a);}
  });
});

$('.table-add').click(function () {addDiaryRow('None', 'null', 'void');});

$('.number-edit').on('keydown',
  function(e){
    var who = $(this);
    if(e.keyCode==13){
      $.ajax({
        type: 'POST',
        url: '/diary',
        data: packDiaryEntry($(this).parent()),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function(data){who.next().html(data.change)}
      });
      return false;
    }
  });

function packDiaryEntry(row) {
  return JSON.stringify({
    title: row.find('.work-title').text(),
    count: row.find('.work-count').text(),
    change: row.find('.work-change').text()
  })
}

function addTableRow(table, values) {
    let template = $('#' + table).find('tr.template');
    let newRow = template.clone(true).removeClass('template').removeAttr('hidden');
    newRow.children().each(function(){
      $(this).html(values[$(this).attr('id')])
    })
    template.before(newRow);
}

