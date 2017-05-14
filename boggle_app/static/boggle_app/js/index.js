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

// Array gathering solution modified from
//    http://stackoverflow.com/questions/4856283/jquery-collect-value-of-list-items-and-place-in-array
function solve() {
    var letters = $(".board_cell").sort(function (a, b) {
        return a.id > b.id;
    }).map(function () {
        return $(this).text();
    }).get();
    $.ajax({
        type: "POST",
        url: $("#board_table").data('solve_url'),
        data: letters,
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