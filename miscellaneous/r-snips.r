library(RColorBrewer)  # great palettes
library(ggplot2)  # plotting


getPalette= colorRampPalette(brewer.pal(9, "Set1"))  # nice palette


ggplot(data, aes(x=V1, y=V2, fill=V1))
    + geom_bar(stat="identity") # don't count; use my values
    + theme(axis.text.x = element_blank()) # remove x axis text
    + labs(x="cuisines", y="# recipes", fill="cuisine") # labels
    + scale_fill_manual(values=getPalette(32)) # use these colours (with 32 values)

ings <- transform(ings, V1=reorder(V1, -V2)) # reorder df by count of V2


require(scales)
+ scale_y_continuous(labels = comma)  # no scientific notation
