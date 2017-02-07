/*
    Planet object for creating dynamic and random planets in Three.js
 */

var Planet = function(planet_seed){
    this.seed = planet_seed;
    this.radius = 100;
    this.widthSegments = 16;
    this.heightSegments = 16;

    this.material = new THREE.MeshBasicMaterial({
      color: this.getColor()
    });

    this.mesh = new THREE.Mesh(new THREE.SphereGeometry(this.radius, this.widthSegments, this.heightSegments), this.material);

    return this;
};

Planet.prototype.getColor = function() {
    console.log('get color');
    // calculate color based on seed
    return 0xffff00;
};
