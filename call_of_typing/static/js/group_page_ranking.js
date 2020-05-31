function group_text_ranking() {

    print('here');
    disappear_song_table();
    appear_text_table();


}

function group_song_ranking() {

    disappear_text_table();
    appear_song_table();

}


function appear_text_table() {

    table = document.querySelector("#group-text-table");
    table.style.display = '';
}

function disappear_text_table() {

    table = document.querySelector("#group-text-table");
    table.style.display = 'none';
}

function appear_song_table() {

    table = document.querySelector("#group-song-table");
    table.style.display = '';
}
function disappear_song_table() {

    table = document.querySelector("#group-song-table");
    table.style.display = 'none';
}