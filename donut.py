from math import cos, sin,pi
import numpy as np 
import time 
import os 


theta_spacing = 0.07
phi_spacing = 0.02

screen_width = 40 
screen_height =40 

R1 = 7/10#1
R2 = 10/10#2 
K2 = 5#5
K1 =  screen_width *K2*3/(8*(R1+R2))


#https://stackoverflow.com/questions/27612545/how-to-change-the-location-of-the-pointer-in-python
def move (y, x):
    print("\033[%d;%dH" % (y, x))

def render_frame(A,B):

    cosA = np.cos(A)
    cosB =  np.cos(B)
    sinA = np.sin(A)
    sinB = np.sin(B)

    output = np.empty((screen_width, screen_height), dtype='<U5')
    output[:,:] = ' '
    zbuffer = np.zeros(shape =(screen_width, screen_height))

    theta = 0 
    while theta < 2*pi:


        costheta = cos(theta)
        sintheta = sin(theta)


        phi = 0 

        while phi < 2*pi:

            cosphi = cos(phi)
            sinphi = sin(phi)

            # (x,y) coordinates of circle 

            circlex = R2 + R1*costheta
            circley = R1*sintheta


            # 3D (x,y,z) coordinate after rotations
            x = circlex *(cosB*cosphi + sinA*sinB*sinphi )
            - circley*cosA*sinB

            y = circlex * (sinB*cosphi - sinA*cosB*sinphi) 
            + circley*cosA*cosB

            z = K2 +circlex*cosA*sinphi + circley*sinA

            ooz = 1/z 




            #(x,y)-coordinate of screen 
            xp =int(screen_width//2 +  K1 * ooz * x )
            yp =int(screen_height//2 - K1* ooz * y )


           

            # Compute luminance 
            L = cosphi *costheta*sinB -cosA*costheta*sinphi - sinA * sintheta + cosB *(cosA*sintheta -costheta*sinA*sinphi)

            # L ranges from -sqrt(2) to +sqrt(2).  If it's < 0, the surface
            # is pointing away from us, so we won't bother trying to plot it.

            if L > 0 :
                # test against the z-buffer.  larger 1/z means the pixel is
                # closer to the viewer than what's already plotted.

                if ooz > zbuffer[xp,yp]:
                    zbuffer[xp,yp]= ooz 
                    luminance_index = int(L*8)
                    # luminance_index is now in the range 0..11 (8*sqrt(2) = 11.3)
                    # now we lookup the character corresponding to the
                    # luminance and plot it in our output:
                    output[xp,yp] = ".,-~:;=!*#$@"[luminance_index]


            phi+= phi_spacing


        theta += theta_spacing 

    
    # Reset cursor postion
    #move(0,0)

    frame = ''

    for j in range(screen_height):
        for i in range(screen_width):
            frame+= output[i,j] 
            
        frame+= '\n'
        
    print(frame, end='')
    



if __name__ == '__main__':
    A,B =  1, 1
    for k in range(1000):
        #print('Itereation: ', k)
        A+= 0.07
        B+= 0.03

        render_frame(A,B)

        #time.sleep(0.008)
        #os.system('cls' if os.name == 'nt' else 'clear')



