$fn=300;

outer=54.0;
inner = 18.5;
hole = 15.0;
thickness = 5.0;
lip=2.0;


difference(){
    union(){
            difference(){
                cylinder(h=thickness,r=inner+5);
                cylinder(h=thickness,r=inner);
            }
            cylinder(h=lip,r=outer);
    }
    
    cylinder(h=thickness,r=hole);
}