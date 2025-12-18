const cvs = document.getElementById("cvs");
const ctx = cvs.getContext("2d");
let img = new Image();
let boxes = [];
let drawing = false;
let sx, sy;

img.src = "/image/" + IMAGE_NAME;
img.onload = () => {
    cvs.width = img.width;
    cvs.height = img.height;
    redraw();
};

fetch("/load_label/" + IMAGE_NAME)
.then(r=>r.json())
.then(d=>{ boxes=d; redraw(); });

function redraw(){
    ctx.clearRect(0,0,cvs.width,cvs.height);
    ctx.drawImage(img,0,0);
    ctx.strokeStyle="red";
    ctx.lineWidth=2;
    boxes.forEach(b=>{
        let [c,x,y,w,h]=b;
        ctx.strokeRect(
            (x-w/2)*cvs.width,
            (y-h/2)*cvs.height,
            w*cvs.width,
            h*cvs.height
        );
    });
}

cvs.onmousedown = e=>{
    drawing=true;
    sx=e.offsetX;
    sy=e.offsetY;
};

cvs.onmouseup = e=>{
    drawing=false;
    let ex=e.offsetX, ey=e.offsetY;
    let x=(sx+ex)/2/cvs.width;
    let y=(sy+ey)/2/cvs.height;
    let w=Math.abs(ex-sx)/cvs.width;
    let h=Math.abs(ey-sy)/cvs.height;
    boxes.push([0,x,y,w,h]);
    redraw();
};

function save(){
    fetch("/save_label/"+IMAGE_NAME,{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify(boxes)
    }).then(()=>alert("已保存"));
}
