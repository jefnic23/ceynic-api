const grid = document.getElementById('image-grid');
var row = 0;
var width = screen.width;

function createRow() {
    var new_row = document.createElement('div');
    new_row.className = 'row';
    grid.append(new_row);
    row++;
}

for (let i = 0; i < pics.length; i++) {
    var col = document.createElement('div');
    col.className = 'col-xs-6 col-sm-4 col-md-4 col-lg-4';

    var pic = document.createElement('img');
    pic.className = "img-responsive";
    pic.src = 'static/pics/' + pics[i];

    col.append(pic);
    grid.children[row].append(col);

    if ((width < 768 && grid.children[row].children.length === 2) || (width >= 768 && grid.children[row].children.length === 3)) {
        createRow();
    }
}