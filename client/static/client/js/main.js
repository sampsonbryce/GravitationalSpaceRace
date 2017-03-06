// list of all players other than you
var playerPositions = {};

// set up socket
var socket;
socketConnect();

//init all variables
var width, height, renderer, scene, controls, camera, player;
width = window.innerWidth;
height = window.innerHeight;
var aspect = width/height;
var clock = new THREE.Clock();
var vectorUp = new THREE.Vector3(0, 1, 0);
var positionUpdateFrameCount = 20;
var frame = 0;

var input = {
    forward: false,
    backward: false,
    left: false,
    right: false
};

const VIEW_ANGLE = 70;
const NEAR = 1;
const FAR = 1000;

const container = $('#container'); // get container div

init(); // initialize environment
animate(); // start animation

function init(){

    //scene
    scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2( 0xcccccc, 0.00025 );

    // renderer
    renderer = new THREE.WebGLRenderer();
    renderer.setClearColor( scene.fog.color );
    renderer.setPixelRatio( window.devicePixelRatio );
    renderer.setSize(width, height);


    // camera
    camera =
        new THREE.PerspectiveCamera(
            VIEW_ANGLE,
            aspect,
            NEAR,
            FAR
        );
    camera.position.z = 500;

    //add controls
    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableZoom = false;
    controls.minDistance = 500;
    controls.maxDistance = 500;

    controls.addEventListener("change", render);

    const redLambertMaterial = new THREE.MeshLambertMaterial({
        color: 0xCC0000
    });

    // create player
    player = new Player(player_name, new THREE.Mesh(new THREE.SphereGeometry(50, 16, 16), redLambertMaterial));

    // create point light
    const pointLight = new THREE.PointLight(0xFFFFFF);
    pointLight.position.x = 10;
    pointLight.position.y = 50;
    pointLight.position.z = 130;

    const ambientLight = new THREE.AmbientLight(0xFFFFFF, 0.3);
    ambientLight.position.x = 1000;
    ambientLight.position.y = 1000;
    ambientLight.position.z = 1000;

    //  GROUND
    var gt = new THREE.TextureLoader().load( "/static/client/textures/checkerboard-square-power-of-2.jpg" );
    gt.minFilter = THREE.LinearFilter;
    var gg = new THREE.PlaneBufferGeometry( 16000, 16000 );
    var gm = new THREE.MeshPhongMaterial( { color: 0xffffff, map: gt } );
    var ground = new THREE.Mesh( gg, gm );
    ground.position.y = -100;
    ground.rotation.x = - Math.PI / 2;
    ground.material.map.repeat.set( 64, 64 );
    ground.material.map.wrapS = THREE.RepeatWrapping;
    ground.material.map.wrapT = THREE.RepeatWrapping;
    // note that because the ground does not cast a shadow, .castShadow is left false
    ground.receiveShadow = true;

    var planet = createPlanet();

    // add everything to scene
    scene.add(planet.mesh);
    scene.add(camera);
    scene.add(player.mesh);
    scene.add(pointLight);
    scene.add(ambientLight);
    scene.add(ground);

    // add dom element to container
    container.append(renderer.domElement);

    window.addEventListener( 'resize', onWindowResize, false );
    document.addEventListener('keydown', move);
    document.addEventListener('keyup', unmove);

    render(); // render scene
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize( window.innerWidth, window.innerHeight );
}

function render(){
    renderer.render(scene, camera);
}

function animate(){
    controls.update();
    requestAnimationFrame(animate);
    update();
    render();
}

function update(){
    updateCamera();
    updatePositions();
}
function updateCamera(){

    var delta = clock.getDelta(); // seconds.
    var moveDistance = 200 * delta; // 200 pixels per second
    var direction = camera.getWorldDirection();

    // move
    if (input.forward){
        player.moveForward(moveDistance, direction);
    }
    if (input.backward){
        player.moveBackward(moveDistance, direction);
    }
    if (input.left)
    {
        player.moveLeft(moveDistance, direction);
    }
    if (input.right)
    {
        player.moveRight(moveDistance, direction);
    }

    controls.target = player.mesh.position;
    camera.lookAt( player.mesh.position );
}

function updatePositions(){
    if(frame > positionUpdateFrameCount){
        frame = 0;
        if (socket.readyState == WebSocket.OPEN){
            console.log('sending position', player.mesh.position)
            socket.send([player_name, JSON.stringify(player.mesh.position)]);
        }
        else{
            console.log('websocket closed');
        }
    }
    else{
        frame += 1;
    }
}

function move(event){
    switch(event.keyCode){
        case 87:
            input.forward = true;
            break;
        case 83:
            input.backward = true;
            break;
        case 65:
            input.left = true;
            break;
        case 68:
            input.right = true;
            break;
        default:
            return;
    }
}

function unmove(event){
    switch(event.keyCode){
        case 87:
            input.forward = false;
            break;
        case 83:
            input.backward = false;
            break;
        case 65:
            input.left = false;
            break;
        case 68:
            input.right = false;
            break;
        default:
            return;
    }
}

function createPlanet(){
    var planet = new Planet(1234);
    return planet;
}

function socketConnect(){
    socket = new WebSocket("ws://" + window.location.host + "/client/");
    socket.onmessage = function(e) {
        var data = JSON.parse(e.data);
        var name = data['name'];

        // if we got our own data
        if(name == player.name){
            return;
        }

        var position = JSON.parse(data['position']);
        console.log('name', name);
        console.log('positon', position);
        if(playerPositions[name]){
            console.log('updating position');
            playerPositions[name].updatePosition(position);
        }
        else{
            console.log('creating player');
            var new_plyr = new Player(name);
            playerPositions[name] = new_plyr;
            playerPositions[name].updatePosition(position);
            scene.add(new_plyr.mesh);
        }
    };

    socket.onclose = function(){
        setTimeout(socketConnect, 1000);
    };
}
