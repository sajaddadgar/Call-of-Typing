function type_ranking() {

    disappear_song_table();
    appear_type_table();


}

function song_ranking() {

    disappear_type_table();
    appear_song_table();

}


function total_ranking() {
    type_table_header = document.querySelector("#type-ranking-table-header");
    type_table_body = document.querySelector("#type-ranking-table-body");
    type_table_header.style.display = 'none';
    type_table_body.style.display = 'none';

}
function group_ranking() {
    type_table_header = document.querySelector("#type-ranking-table-header");
    type_table_body = document.querySelector("#type-ranking-table-body");
    type_table_header.style.display = 'none';
    type_table_body.style.display = 'none';

}

function appear_type_table() {

    table = document.querySelector("#type-table");
    table.style.display = '';
}

function disappear_type_table() {

    table = document.querySelector("#type-table");
    table.style.display = 'none';
}

function appear_song_table() {

    table = document.querySelector("#song-table");
    table.style.display = '';
}
function disappear_song_table() {

    table = document.querySelector("#song-table");
    table.style.display = 'none';
}