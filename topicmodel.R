setwd("E:/work")
#import packages
library(tidyr)
library(ldatuning)
library(SnowballC) 
library(rvest)
library(NLP)
library(tm)
library(dplyr)
library(tidytext)
library(topicmodels)
library(readxl)
library(readr)
library(quanteda)
library(gofastr)
library(ggplot2)
library(dplyr)
library(udpipe)
#import dataset
annals <- read_excel("F:/LDA_ROBUST_segment.xlsx")
View(annals)
#convert dataset to corpus
anCorpus <- Corpus(VectorSource(annals$textnew))
#convert corpus to DocumentTermMatrix
andtm <- DocumentTermMatrix(anCorpus)
#find words occuring less than 10 time
word <- findFreqTerms(andtm, lowfreq = 1, highfreq = 10)
#function remove terms over 50%
removeCommonTerms <- function (x, pct) 
{
  stopifnot(inherits(x, c("DocumentTermMatrix", "TermDocumentMatrix")), 
            is.numeric(pct), pct > 0, pct < 1)
  m <- if (inherits(x, "DocumentTermMatrix")) 
    t(x)
  else x
  t <- table(m$i) < m$ncol * (pct)
  termIndex <- as.numeric(names(t[t]))
  if (inherits(x, "DocumentTermMatrix")) 
    x[, termIndex]
  else x[termIndex, ]
}
#run removeCommonTerms function
andtm<-removeCommonTerms(andtm ,.5)
andtm <- dtm_remove_terms(andtm, terms = as.vector(word), remove_emptydocs = FALSE)
k<-100
##run model
Gibbs <- LDA(andtm, k = k, method = "Gibbs",
            control = list(alpha = 0.5,delta = 0.1,seed = 1234, iter = 400))

##check topics
kic_topics <- tidy(Gibbs, matrix = "beta")

kic_top_terms <- kic_topics %>%
  group_by(topic) %>%
  slice_max(beta, n = 20) %>% 
  ungroup() %>%
  arrange(topic, -beta)
#save top_terms_each_topic
write.table(kic_top_terms,"robust_top_terms_each_topic.csv",row.names=FALSE,col.names=TRUE,sep=",")

# kic_document
kic_documents <- tidy(Gibbs, matrix = "gamma")
kic_documents<-spread(kic_documents, key=topic, value=gamma)
#save top_doc_each_topic
write.table(kic_documents,"robust_top_doc_each_topic.csv",row.names=FALSE,col.names=TRUE,sep=",")