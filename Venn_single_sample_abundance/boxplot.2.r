Args <- commandArgs()
options(stringsAsFactors=F)

re  <- read.table(Args[3],header=T,sep="\t",check.names = F,row.names=1,quote="")
#re[,2] <- re[,2]/sum(re[,2])
#re[,3] <- re[,3]/sum(re[,3])
#re[,2:3] <- sapply(2:3,function(x) re[,x] <-re[,x]/sum(re[,x]))
otu <- re
otu_pec <- otu
otuname <- rownames(otu)
colnamess <- colnames(otu)
otu_pec <- sapply(1:ncol(re),function(x) otu_pec[,x] <-otu[,x]/sum(otu[,x]))
rownames(otu_pec) <- otuname
colnames(otu_pec) <- colnamess
write.table(otu_pec,file=paste(Args[3],".group.ok.txt",sep=""),quote=F,sep="\t",row.names=T)

