require(scales)
library(ggplot2)
library(RColorBrewer)

# top ingredients
ings <- read.csv("top20_ingredients.tsv", header=F, sep="\t")
ings <- transform(ings, V1=reorder(V1, -V2))


ggplot(ings, aes(x=V1, y=V2, fill=V1)) + geom_bar(stat="identity") + theme(axis.text.x = element_blank()) + labs(x="ingredients", y="# occurrences in recipes", fill="top ingredients") + scale_fill_manual(values=getPalette(32))+ scale_y_continuous(labels = comma)


# top verbs
events <- read.csv("top20_events.tsv", header=F, sep="\t")
events <- transform(events, V2=reorder(V2, -V1))
ggplot(events, aes(y=V1, x=V2, fill=V2)) + geom_bar(stat="identity") + theme(axis.text.x = element_blank()) + labs(x="verbs", y="# occurrences in recipes", fill="top verbs") + scale_fill_manual(values=getPalette(32))+ scale_y_continuous(labels = comma)


# ings by cuisine
cc <- read.csv("top10_ings_per_cuisine.tsv", sep="\t")
ggplot(cc, aes(x=ingredient, fill=ingredient, color=ingredient, y=fraction, label=ingredient)) + geom_bar(stat="identity") + facet_wrap(~ cuisine, scales="free_x")  + scale_fill_manual(values=getPalette(37)) + theme(axis.text.x = element_blank()) + scale_color_manual(values=c("black", "grey", "black","grey", "black","grey", "black","grey", "black","grey", "black","grey", "black","grey", "black","grey", "black","grey", "black","grey", "black","grey", "black","grey", "black","grey", "black","grey", "black","grey","black","grey","black","grey", "black","grey", "black", "grey")) + scale_y_continuous(labels=percent)
