#library(tibble)
library(ggplot2)

loans = read.table("core_data.csv", header = TRUE, sep = ',')
model = read.table("model_predictions.csv", header = TRUE, sep = ',')


loans$model = model$model

plot = ggplot(loans, aes(x=period, y=naive))+
    geom_ribbon(aes(period, ymax=maximum, ymin=minimum), fill="gray", alpha = 0.25)+
    geom_line(aes(period, phonotactic))+
    geom_line(aes(period, naive))+
    theme_bw()

