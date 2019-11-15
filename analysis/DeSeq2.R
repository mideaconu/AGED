#
# Analysis of Mayo Clinic RNA-seq data for Cerebellum (CBE) and Temporal Cortex (TCX)
# Author: Prof Kevin Bryson
#

library("DESeq2")
library("plyr")

cbeCounts <- as.matrix(read.csv("MayoRNAseq_RNAseq_CBE_geneCounts.tsv", sep="\t", row.names="ensembl_id"))
tcxCounts <- as.matrix(read.csv("MayoRNAseq_RNAseq_TCX_geneCounts.tsv", sep="\t", row.names="ensembl_id"))

cbeSamples <- read.csv("MayoRNAseq_RNAseq_CBE_covariates.csv", row.names=1)
tcxSamples <- read.csv("MayoRNAseq_RNAseq_TCX_covariates.csv", row.names=1)

rownames(cbeSamples) <- paste0('X', rownames(cbeSamples))
rownames(tcxSamples) <- paste0('X', rownames(tcxSamples))

cbeSamples <- cbeSamples[!is.na(cbeSamples['Diagnosis']) & !is.na(cbeSamples['Tissue']),]
tcxSamples <- tcxSamples[!is.na(tcxSamples['Diagnosis']) & !is.na(tcxSamples['Tissue']),]

# With removal of these 'NA' samples -
# all sample names are not columns in count matrix so just select these ones.
# in the count matrices (NB - in the order they occur in the samples).

cbeCounts <- cbeCounts[, rownames(cbeSamples)]
tcxCounts <- tcxCounts[, rownames(tcxSamples)]

# Correction of differences in sample column names between the different samples

colnames(cbeSamples)[5] <- "Gender"
colnames(tcxSamples)[8] <- "Flowcell"

# Create final sample and count data objects

samples <- rbind(cbeSamples, tcxSamples)
counts <- cbind(cbeCounts, tcxCounts)

# Ideally Diagnosis factors should not have spaces in level names and control should be given first

samples$Diagnosis <- revalue(samples$Diagnosis, c("Pathologic Aging" = "PA"))
samples$Diagnosis <- relevel(samples$Diagnosis, ref = "Control")

dds <- DESeqDataSetFromMatrix(countData = counts, colData = samples, design = ~Tissue + Diagnosis)

# Filter off genes that have row count totals < 10

keep <- rowSums(counts(dds)) >= 10
dds <- dds[keep,]

# Generate data

dds <- DESeq(dds)

vst <- vst(dds, blind = FALSE)

write.csv(samples, file="mayo_samples.csv")
write.csv(assay(vst), file="mayo_log_expression.csv")