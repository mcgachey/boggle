function updateCell(cell_id) {
    var letter = window.prompt("Enter a single letter.", "-");
    letter = scrubInput(letter)
    $(cell_id).text(letter)
}

function scrubInput(letter) {
    letter = letter.toUpperCase()
    if (letter.length != 1) {
        return "-";
    }
    if (letter.charCodeAt(0) < "A".charCodeAt(0) || letter.charCodeAt(0) > "Z".charCodeAt(0)) {
        return "-";
    }
    return letter;
}

function randomize() {
    $(".board_cell").sort(function (a, b) {
        return a.id > b.id;
    }).each(function (cell) {
        $(this).text(randomChar());
    })
}

function solve() {
    var letters = []
    for (row=0; row<4; row++) {
        for (col=0; col<4; col++) {
            letters.push($("#board_cell_" + row + "_" + col).text())
        }
    }
    $.ajax({
        type: "POST",
        url: $("#board_table").data('solve_url'),
        data: JSON.stringify(letters),
        dataType: "json"
    }).done(function (words) {
        console.log("Words: " + words);
        var results = $("#results")
        results.html("<P><B>Matching Words</B></P>");
        for (idx in words) {
            results.html("<P>" + results.html() + words[idx] + "</P>");
        }
    }).fail(function (message) {
        window.alert("Error: " + message.responseText);
    });
}

function randomChar() {
    var valid = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return valid.charAt(Math.random() * valid.length)
}