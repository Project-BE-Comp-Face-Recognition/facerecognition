function checkFiles(files) {       
    if(files.length<5) {
        alert("Select at leat 10 Images");
        
        let list = new DataTransfer;
        for(let i=0; i<10; i++)
           list.items.add(files[i]) 

        document.getElementById('files').files = list.files
    }       
}