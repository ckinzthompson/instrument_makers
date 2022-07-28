$fn=100;
pad = 0.1;
module screw(screwthread_h){
    screwhead_h = 3.9;
    screwhead_r = 4.40 +pad/2;
    //screwthread_h = 11.4;
    screwthread_r = 2.40 +pad/2;
    
    union(){
        translate([0,0,screwthread_h]){
            union(){
            cylinder(h=screwhead_h, r1=screwthread_r, r2=screwhead_r, center=false);
            translate([0,0,screwhead_h]){
                cylinder(h=screwhead_h*10, r=screwhead_r, center=false);
            }
            }
        }
        translate([0,0,1])
        cylinder(h=screwthread_h, r=screwthread_r, center=false);
        
    }
}
module testtube(tube_h){
    //tube_h = 98.425;
    tube_r = 7.8+pad/2.;
    tube_c = 7.8+pad/2;
    tube_fn = 80;
    cap_h = 18.85;
    cap_r = 10.05;
    translate([0,0,tube_c]){
        union(){
            cylinder(h=tube_h-tube_c, r=tube_r, center=false);
            sphere(r=tube_c);
            translate([0,0,tube_h-cap_h-tube_c]){
                cylinder(h=cap_h, r=cap_r, center=false);
            }
        }
    }
}
inch=25.4;
base = 1.*inch;
back_h = 1.5*inch;
difference(){
translate([0,0,-.25*inch]){
difference(){
    //this
    union(){
        translate([0,0,base/2]){
            cube([base,base,base],center=true);
        }
        translate([base/4,0,back_h/2]){
            cube([base/2,base,back_h],center=true);
        }
    }
    //minus
    
    translate([-.025*inch,0,.6*inch]){
        rotate([0,15,0]){
            testtube(98.425);
        }
    }
    
    //minus
    translate([-.2*inch,0,-1]){
        screw(12);
    }
    
    //minus
    cube([base,base,.5*inch],center=true);
}
}
    //bevel
    translate([0,0,-pad]){
    difference(){
        cylinder(h=back_h*1.25,r=base/2*1.5);
        cylinder(h=back_h*1.25,r=base/2);
    }}
}
