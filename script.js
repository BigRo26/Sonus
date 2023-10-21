const dragArea = document.querySelector('.drag-area');
const dragText = document.querySelector('.header');

let button = document.querySelector(".button");
let input = document.querySelector('input');

let file;

button.onclick = () => {
    input.click();
};

input.addEventListener('change', function(){
    file = this.files[0];
    let fileType = file.type;
    valid_exts = ['audio/wav', 'video/quicktime']
    if(valid_exts.includes(fileType)==false){
        alert("This is not a valid file type")
    } else{

    };
});

dragArea.addEventListener('dragover', (event) =>{
    console.log("FILE IN DRAG AREA");
    event.preventDefault();
    dragText.textContent = "Release to Upload";
    dragArea.classList.add('active');
});

dragArea.addEventListener('dragleave', () =>{
    console.log("file left area");
    dragText.textContent = "Drag & Drop";
    dragArea.classList.remove('active');
});

dragArea.addEventListener('drop', (event)=> {
    event.preventDefault();
    dragArea.classList.remove('active');
    file = event.dataTransfer.files[0];
    let fileType = file.type;
    valid_exts = ['audio/wav', 'video/quicktime']
    if(valid_exts.includes(fileType)==false){
        alert("This is not a valid file type")
    } else{

    };
});

 