function text_ranking() {

    disappear_song_table();
    disappear_song_group_table();
    disappear_text_group_table();
    appear_text_table();


}

function song_ranking() {

    disappear_text_table();
    disappear_song_group_table()
    disappear_text_group_table()
    appear_song_table();

}

function group_text_ranking() {
    disappear_song_group_table()
    disappear_song_table()
    disappear_text_table()
    appear_text_group_table()

}

function group_song_ranking() {
    disappear_text_group_table()
    disappear_song_table()
    disappear_text_table()
    appear_song_group_table()

}


function appear_text_table() {

    let table = document.querySelector("#text-table");
    table.style.display = '';
}

function disappear_text_table() {

    let table = document.querySelector("#text-table");
    table.style.display = 'none';
}

function appear_song_table() {

    let table = document.querySelector("#song-table");
    table.style.display = '';
}

function disappear_song_table() {

    let table = document.querySelector("#song-table");
    table.style.display = 'none';
}

function appear_text_group_table() {

    let table = document.querySelector("#text-group-table");
    table.style.display = '';
}

function disappear_text_group_table() {

    let table = document.querySelector("#text-group-table");
    table.style.display = 'none';
}

function appear_song_group_table() {

    let table = document.querySelector("#song-group-table");
    table.style.display = '';
}

function disappear_song_group_table() {

    let table = document.querySelector("#song-group-table");
    table.style.display = 'none';
}