import pickle
import math
import streamlit as st

st.header('LR 1280')
with open("data.pkl", "rb") as f:
    data = pickle.load(f)

for i in data[30]:
    data[30][i] = data[30][i].rename(columns={'Radius (m)': '0'})
for i in data[15]:
    data[15][i] = data[15][i].rename(columns={'Radius (m)': '0'})


list_angles=[i for i in data][::-1]
final_angles=list_angles[2:4]+[15,30]+list_angles[4:]
#-------------------------------------------------------------->> input
r = st.number_input("Enter Radius (m)", min_value=1.0)
h = st.number_input("Enter Height (m)",min_value=1.0)

l=(h**2-r**2)**(1/2)
try:
        
    # Calculate angle in radians
    angle_rad = math.acos(r/l) 

    # Convert to degrees
    angle_deg = math.degrees(angle_rad)

    print(f"Angle in degrees: {angle_deg}")
    print('radius:',r)

    capacity=[]
    #------------------------------------> main-boom
    l1=[float(i[:-1]) for i in data['main-boom'].columns[1:][:8]]
    l2=[float(i) for i in data['main-boom'].columns[1:][8:]]
    length=l1+l2
    names=list(data['main-boom'].columns[1:])
    for i,le in enumerate(length):
        if le>=l:
            break
    col=names[i]
    df=data['main-boom']
    for ra in list(df['Radius']):
        if ra>=r:
            break
    capacity.append([max(df[df['Radius']==ra][col]),0,le,'main-boom'])

    #---------------------------------------> l-boom
    for le in [float(i) for i in data['l-boom'].columns[:-1]]:
        if le>=l:
            break
    col=str(le)
    df=data['l-boom']
    for ra in list(df['0']):
        if ra>=r:
            break
    capacity.append([max(df[df['0']==ra][col]),0,le,'l-boom'])
    #---------------------------------------------> all angles
    import pandas as pd
    def col(df,r,l):
        boom_cols = sorted(
            int(c) for c in df.columns[1:]
            if pd.notna(c) and c != '0'
        )
        for le in boom_cols:
            if le>=l:
                break
        col=str(le)
        row=[]
        for ra in list(df['0']):
            if ra>r:
                row.append(ra)
        return max(df[df['0'].isin(row)][col]),col

    cc=[]
    for a in final_angles[2:]:
        df=data[a]
        mxca,mxjl,mxbl=0,0,0
        for k in list(df.keys()):
            nl=l-k
            cap,jl=col(df[k],r,nl)
            #print(a,'|  mainboom:',k,'  |  jib len:',jl,' |  radius=',r,'  ||  capacity:',cap)
            if mxca<cap:
                mxca=cap
                mxjl=jl
                mxbl=k
        capacity.append([(mxca,mxjl,mxbl),a])
    st.write(f"Angle in degrees: {angle_deg}")
    st.write('length:',l)
    st.write('radius:',r)
    capac=[]
    for cap in capacity:
        if len(cap)==4:
            c,jll,bl,aa=cap
            col1,col2=st.columns(2)
            capac.append(c)
        else:
            cc,aa=cap
            c,jll,bl=cc
            capac.append(c)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("images/main-boom.png")
        for cap in capacity:
            if cap[-1]=='main-boom':
                break
        with st.expander('check'):
            c,jll,bl,aa=cap
            st.write('capacity:',c)
            st.write('boom length:',bl)
            st.write('jib len:',jll)
        st.write('max:',max(capac))
        st.write('min:',min(capac))
                

    with col2:
        st.image("images/l-boom.png")
        for cap in capacity:
            if cap[-1]=='l-boom':
                break
        with st.expander('check'):
            c,jll,bl,aa=cap
            st.write('capacity:',c)
            st.write('boom length:',bl)
            st.write('jib len:',jll)

    with col3:
        st.image("images/luffing-jib.png")
        with st.expander('check'):
            for cap in capacity:
                if type(cap[-1])==int:
                    cc,aa=cap
                    c,jll,bl=cc
                    st.write('Angle:',aa)
                    st.write('capacity:',c)
                    st.write('boom length:',bl)
                    st.write('jib len:',jll)
                    st.divider()
except:
    st.write("Give full info required..")