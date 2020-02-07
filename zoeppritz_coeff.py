#zoeppritz_coeff.py

#================================================================================

#Import relevant modules
import numpy as np

#Define zoeppritz function
def zoeppritz(p,iso1,iso2):
    """ 
        This function generates a full matrix of Zoeppritz reflection/transmission coefficients for isotropic media
        This is a translation of the MATLAB script provided by Chris Chapman
       
        Inputs:
        p    - float, horizontal slowness
        
        iso1 - layer 1 properties in the form below
        
               [p wave velocity, s wave velocity, density]
               
        iso1 - layer 2 properties in the same form
                 

               
        Outputs:
        output - full 6x6 matrices of coefficients in the form below
                 Rmatrix = [[ V1V1,  0  , P1V1, V2V1,  0  , P2V1],
                            [  0  , H1H1,  0  ,  0  , H2H1,  0  ],
                            [ V1P1,  0  , P1P1, V2P1,  0  , P2P1],
                            [ V1V2,  0  , P1V2, V2V2,  0  , P2V2],
                            [  0  , H1H2,  0  ,  0  , H2H2,  0  ],
                            [ V1P2,  0  , P1P2, V2P2,  0  , P2P2]]
                            
                 The first 3 columns correspond to waves incident from medium 1
                 The last 3 columns correspond to waves incident from medium 2
                 The first 3 rows correspond to waves generate in medium 1
                 The last 3 rows correspond to waves generate in medium 2
                 The waves are ordered SV, SH and P
                 The SH-SV and P-SV entries in the Rmatrix are zero
    """

    
    #Create output matrix
    Rmatrix = np.zeros((6,6))
    
    #Extract densities
    rho1 = iso1[2]
    rho2 = iso2[2]
    p2 = p*p
    
    #Free surface
    if rho1 == 0:
        # print('Free upper surface')
        
        #Free fluid
        if iso2[1] == 0:
            Rmatrix[6,6] = -1
            
        #Free solid
        else:
            qa2 = np.sqrt(((1/iso2[0]) - p)*((1/iso2[0]) + p))
            qb2 = np.sqrt(((1/iso2[1]) - p)*((1/iso2[1]) + p))
            Omega2 = qb2*qb2 - p2
            DeltaPV = 4*p2*qa2*qb2 + (Omega2**2)
            
            Rmatrix[5,5] = (4*p2*qa2*qb2 - (Omega2**2))/DeltaPV
            Rmatrix[3,3] = Rmatrix[5,5]*(-1)
            Rmatrix[3,5] = 4*p*Omega2*np.sqrt(qa2*qb2)/DeltaPV
            Rmatrix[5,3] = Rmatrix[3,5]
            Rmatrix[4,4] = 1
    
    #Free lower surface        
    elif rho2 == 0:
        # print('Free lower surface')
        
        #Fluid on top of free base
        if iso1[2] == 0:
            Rmatrix[2,2] = -1
            
        #Solid on free surface
        else:
            qa1 = np.sqrt(((1/iso1[0]) - p)*((1/iso1[0]) + p))
            qb1 = np.sqrt(((1/iso1[1]) - p)*((1/iso1[1]) + p))
            Omega1 = qb1*qb1 - p2
            DeltaPV = 4*p2*qa1*qb1 + (Omega1**2)
            
            Rmatrix[2,2] = (4*p2*qa1*qb1 - (Omega1**2))/DeltaPV
            Rmatrix[0,0] = Rmatrix[2,2]*(-1)
            Rmatrix[0,2] = 4*p*Omega1*np.sqrt(qa1*qb1)/DeltaPV
            Rmatrix[2,0] = Rmatrix[0,2]
            Rmatrix[1,1] = 1
    
    #Fluid on top
    elif iso1[1] == 0:
    
        #fluid-fluid
        if iso2[1] == 0:
            # print('Fluid - Fluid')
            qa1 = np.sqrt(((1/iso1[0]) - p)*((1/iso1[0]) + p))
            qa2 = np.sqrt(((1/iso2[0]) - p)*((1/iso2[0]) + p))
            DeltaA = (rho2*qa1) + (rho1*qa2)
            
            Rmatrix[2,2] = ((rho2*qa1) - (rho1*qa2))/DeltaA
            Rmatrix[5,5] = Rmatrix[2,2]
            Rmatrix[2,5] = 2*np.sqrt(rho1*rho2*qa1*qa2)/DeltaA
            Rmatrix[5,2] = Rmatrix[2,5]
            
        #Fluid - solid
        else:
            # print('Fluid - Solid')
            qa1 = np.sqrt(((1/iso1[0]) - p)*((1/iso1[0]) + p))
            qa2 = np.sqrt(((1/iso2[0]) - p)*((1/iso2[0]) + p))
            qb2 = np.sqrt(((1/iso2[1]) - p)*((1/iso2[1]) + p))
            Omega2 = qb2*qb2 - p2
            Fa1 = np.sqrt(2*rho1*qa1)
            Fa2 = np.sqrt(2*rho2*qa2)
            Fb2 = np.sqrt(2*rho2*qb2)
            DeltaPV = 4*p2*qa2*qb2 + (Omega2**2) + rho1*qa2/(rho2*(iso2[1]**4)*qa1)
            
            Rmatrix[2,2] = (4*p2*qa2*qb2 + (Omega2**2) - ((rho1*qa2)/(rho2*(iso2[1]**4)*qa1)))/DeltaPV
            Rmatrix[3,3] = ((-4)*p2*qa2*qb2 + (Omega2**2) + (rho1*qa2/(rho2*(iso2[1]**4)*qa1)))/DeltaPV
            Rmatrix[5,5] = (4*p2*qa2*qb2 - (Omega2**2) + (rho1*qa2/(rho2*(iso2[1]**4)*qa1)))/DeltaPV
            Rmatrix[2,5] = Fa1*Fa2*Omega2/(qa1*rho2*(iso2[1]**2)*DeltaPV)
            Rmatrix[5,2] = Rmatrix[2,5]
            Rmatrix[3,5] = 2*p*Fa2*Fb2*Omega2/(rho2*DeltaPV)
            Rmatrix[5,3] = Rmatrix[3,5]
            Rmatrix[2,3] = (-2)*p*Fa1*Fb2*qa2/(qa1*rho2*(iso2[1]**2)*DeltaPV)
            Rmatrix[3,2] = Rmatrix[2,3]
            Rmatrix[4,4] = 1
    
    #Fluid on bottom
    #Solid - fluid
    elif iso2[1] == 0:
        # print('Solid - Fluid')
        qa1 = np.sqrt(((1/iso1[0]) - p)*((1/iso1[0]) + p))
        qb1 = np.sqrt(((1/iso1[1]) - p)*((1/iso1[1]) + p))
        qa2 = np.sqrt(((1/iso2[0]) - p)*((1/iso2[0]) + p))
        Omega1 = qb1*qb1 - p2
        Fa1 = np.sqrt(2*rho1*qa1)
        Fb1 = np.sqrt(2*rho1*qb1)
        Fa2 = np.sqrt(2*rho2*qa2)
        DeltaPV = 4*p2*qa1*qb1 + (Omega1**2) + rho2*qa1/(rho1*(iso1[1]**4)*qa2)
        
        Rmatrix[5,5] = (4*p2*qa1*qb1 + (Omega1**2) - (rho2*qa1)/(rho1*(iso1[1]**4)*qa2))/DeltaPV
        Rmatrix[0,0] = (-4*p2*qa1*qb1 + (Omega1**2) + (rho2*qa1)/(rho1*(iso1[1]**4)*qa2))/DeltaPV
        Rmatrix[2,2] = (4*p2*qa1*qb1 - (Omega1**2) + (rho2*qa1)/(rho1*(iso1[1]**4)*qa2))/DeltaPV
        Rmatrix[2,5] = (Fa1*Fa2*Omega1)/(qa2*rho1*(iso1[1]**2)*DeltaPV)
        Rmatrix[5,2] = Rmatrix[2,5]
        Rmatrix[0,2] = (2*p*Fa1*Fb1*Omega1)/(rho1*DeltaPV)
        Rmatrix[2,0] = Rmatrix[0,2]
        Rmatrix[5,0] = (-2*p*Fa2*Fb1*qa1)/(qa2*rho1*(iso1[1]**2)*DeltaPV);
        Rmatrix[0,5] = Rmatrix[5,0];
        Rmatrix[1,1] = 1;
    
    #Solid - solid
    else:
        # print('Solid - Solid')
        qa1 = np.sqrt(((1/iso1[0]) - p)*((1/iso1[0]) + p))
        qb1 = np.sqrt(((1/iso1[1]) - p)*((1/iso1[1]) + p))
        qa2 = np.sqrt(((1/iso2[0]) - p)*((1/iso2[0]) + p))
        qb2 = np.sqrt(((1/iso2[1]) - p)*((1/iso2[1]) + p))
        
        Aap = rho2*qa1 + rho1*qa2
        Abp = rho2*qb1 + rho1*qb2
        Aam = rho2*qa1 - rho1*qa2
        Abm = rho2*qb1 - rho1*qb2
        mu1 = rho1*(iso1[1]**2)
        mu2 = rho2*(iso2[1]**2)
        B1 = mu1 - mu2
        B2 = B1*(-1)
        C1p = 2*p*(B1*(p2 + qa1*qb1) - rho1)
        C1m = 2*p*(B1*(p2 - qa1*qb1) - rho1)
        C2p = 2*p*(B2*(p2 + qa2*qb2) - rho2)
        C2m = 2*p*(B2*(p2 - qa2*qb2) - rho2)
        D = p2*((rho1 + rho2)**2)
        E1 = rho1 - 2*p2*B1
        E2 = rho2 - 2*p2*B2
        Fa1 = np.sqrt(2*rho1*qa1)
        Fa2 = np.sqrt(2*rho2*qa2)
        Fb1 = np.sqrt(2*rho1*qb1)
        Fb2 = np.sqrt(2*rho2*qb2)
        Gbp = mu1*qb1 + mu2*qb2
        Gbm = mu1*qb1 - mu2*qb2
        Hb1 = np.sqrt(2*mu1*qb1)
        Hb2 = np.sqrt(2*mu2*qb2)

        DeltaPV = Aap*Abp - C1p*C2p + D
        DeltaH = Gbp

        Rmatrix[2,2] = (Aam*Abp + C1m*C2p - D)/DeltaPV                                  #P1P1
        Rmatrix[5,5] = (-Aam*Abp + C1p*C2m - D)/DeltaPV                                 #P2P2
        Rmatrix[0,0] = (-Aap*Abm - C1m*C2p + D)/DeltaPV                                 #V1V1
        Rmatrix[3,3] = (Aap*Abm - C1p*C2m + D)/DeltaPV                                  #V2V2
        Rmatrix[2,5] = Fa1*Fa2*(qb1*E2 + qb2*E1)/DeltaPV                                #P2P1
        Rmatrix[5,2] = Rmatrix[2,5]                                                     #P1P2
        Rmatrix[0,3] = Fb1*Fb2*(qa1*E2 + qa2*E1)/DeltaPV                                #V2V1
        Rmatrix[3,0] = Rmatrix[0,3]                                                     #V1V2
        Rmatrix[0,2] = -p*Fa1*Fb1*(2*qa2*qb2*E1*B2 + E2*(E2 - rho1))/(rho1*DeltaPV)     #P1V1
        Rmatrix[2,0] = Rmatrix[0,2]                                                     #V1P1
        Rmatrix[3,5] = -p*Fa2*Fb2*(2*qa1*qb1*E2*B1 + E1*(E1 - rho2))/(rho2*DeltaPV)     #P2V2
        Rmatrix[5,3] = Rmatrix[3,5]                                                     #V2P2
        Rmatrix[2,3] = -p*Fa1*Fb2*(2*B2*qb1*qa2 + E1 - rho2)/DeltaPV                    #V2P1
        Rmatrix[3,2] = Rmatrix[2,3]                                                     #P1V2
        Rmatrix[0,5] = -p*Fa2*Fb1*(2*B1*qb2*qa1 + E2 - rho1)/DeltaPV                    #P2V1
        Rmatrix[5,0] = Rmatrix[0,5]                                                     #V1P2
        Rmatrix[1,1] = Gbm/DeltaH                                                       #H1H1
        Rmatrix[4,4] = -Gbm/DeltaH                                                      #H2H2
        Rmatrix[1,4] = Hb1*Hb2/DeltaH                                                   #H2H1
        Rmatrix[4,1] = Rmatrix[1,4]                                                     #H1H2
        
    return Rmatrix

