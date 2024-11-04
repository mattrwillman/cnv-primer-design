ags <- read.table("AGS2000_full_table.tsv", 
                  header = TRUE, 
                  comment.char = "", 
                  skip = 2,
                  sep = "\t",
                  fill = TRUE, 
                  quote = "", 
                  stringsAsFactor = FALSE)

hil <- read.table("Hilliard_full_table.tsv", 
                  header = TRUE, 
                  comment.char = "", 
                  skip = 2,
                  sep = "\t",
                  fill = TRUE, 
                  quote = "", 
                  stringsAsFactor = FALSE)

colnames(ags)[1] <- "ID"
colnames(hil)[1] <- "ID"

str(ags)


# Find copy number variants.
## For 2 individuals, subtraction could be used to identify copy number variants.
## Standard deviation is used instead to scale code to include more than 2 individuals.

g1 <- ags
g2 <- hil

t1 <- table(g1$ID) |> data.frame()
t2 <- table(g2$ID) |> data.frame()
colnames(t1) <- c("ID", "cn1")
colnames(t2) <- c("ID", "cn2")
cn <- merge(t1, t2, by = "ID")
cn$sd <- apply(cn[2:3], 1, sd)
cnv <- cn[cn$sd != 0, ]

# Extract bed for CNVs

cnv.hilref <- hil[hil$ID %in% cnv$ID, ]
cnv.bed <- cnv.hilref[, c("Sequence", "Gene.Start", "Gene.End")]
cnv.bed$Name <- make.unique(cnv.hilref$ID, ".")

# Sort gene coordinates
for (i in 1:length(rownames(cnv.bed))) {
  row_i <- cnv.bed[i, ]
  start_i <- min(row_i[2:3])
  end_i <- max(row_i[2:3])
  row_i$Gene.Start <- start_i
  row_i$Gene.End <- end_i
  cnv.bed[i, ] <- row_i
}

cnv.bed <- cnv.bed[order(cnv.bed$Gene.Start), ]
cnv.bed <- cnv.bed[order(cnv.bed$Sequence), ]
cnv.bed <- cnv.bed[!is.na(cnv.bed$Gene.Start), ]

# Subset first copy as reference
cnv.bed.single <- cnv.bed[str_detect(cnv.bed$Name, "\\.", negate = TRUE), ]

write.table(cnv.bed, "CNV_HilliardRef.bed", sep = "\t",
            col.names = FALSE, row.names = FALSE, quote = FALSE)

write.table(cnv.bed.single, "CNV_HilliardRef_singles.bed", sep = "\t", 
            col.names = FALSE, row.names = FALSE, quote = FALSE)
