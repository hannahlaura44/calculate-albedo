# calculate the average DN (digital number) of an image IMG.
def calc_avg_DN(img): 
    imarray=num.array(img)
    x_len = imarray[:,0,0].size
    y_len = imarray[0,:,0].size
    # initialize array to Nan
    DN_array = num.empty((x_len,y_len,))
    DN_array[:] = num.NAN
    for i in range(0,x_len):
        for j in range(0,y_len):
            red = hex(imarray[i,j,0])
            green = (format(imarray[i,j,1],'x'))
            blue = (format(imarray[i,j,2],'x'))
            rgb_int = int(red+green+blue, 16)
            # print "rgb_int is ",rgb_int
            DN_array[i,j] = rgb_int
            # print imarray[i,j]

    # find the average DN
    DN_avg = num.average(DN_array)
    print "DN_avg is ",DN_avg
    return DN_avg

# DN_avg = calc_avg_DN(img)