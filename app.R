#Dependencies
library(shiny)
library(COVID19)
library(incidence)
library(ggplot2)
library(dplyr)

#First, define some functions to be called in the app

#Function to convert the cumulative incidence data from the COVID19 package
#to and incidence object
#iso is a country's iso code, so DE for Germany, FR for France, etc.
incidenceData <- function(iso){
  
  #COVID19 data for a given country
  RAW.DATA <- covid19(iso)
  
  #Convert from cumulative cases to daily cases
  RAW.CASES <- diff(RAW.DATA$confirmed)
  CASES <- c(RAW.DATA$confirmed[1], RAW.CASES)
  
  #Extract the dates
  DATES <- RAW.DATA$date
  nDATES <- length(DATES)
  
  #Create an empty vector of class "Date"
  DATA <- integer(0)
  class(DATA) <- "Date"
  
  #Convert from daily cases to "list line" format, which contains a date
  #for each case. This is the required format for the incidence package
  #Clean this up later to eliminate for loop
  for(i in 1:nDATES){
    if(CASES[i]>0) {
      DAY <- rep(DATES[i], CASES[i])
      DATA <- c(DATA, DAY)
    }
  }
  
  #Create the incidence object and return it
  return(incidence(DATA))
  
}

#A function that returns different plot types based on user input
#anl is a user chosen analysis type (currently only 4 options)
#dat is a user chosen data source (currently only 2 options)
plotSwitch <- function(AN, DATASET){
  
  ANL <- switch(AN,
               "Incidence curve" = 1,
               "Incidence curve + model fit" = 2
  )
  
  if(ANL == 1){
    
    #Plot an incidence curve
    plot(DATASET, border = "white")
    
  } else if(ANL == 2) {
    
    #Fit Log-linear models and estimate an optimal split point between
    #growth and decline phases of the epidemic
    FOS <- fit_optim_split(DATASET)
    
    #Plot the incidence curve together with the fitted growth and decay curves
    plot(DATASET, border = "white") %>%
      add_incidence_fit(FOS$fit)
    
  }
}

#Server component of app
server <- function(input, output, session) {
  
  #Create a new data frame with the user-selected data source
  selectedData <- reactive({
    
    #Get the iso code based on the user's selected country
    CC <- switch(input$CTY,
                 "France" = "FR",
                 "Germany" = "DE",
                 "Italy" = "IT",
                 "Spain" = "ES"
    )
    
    #Pass the iso code to incidenceData to return an incidence object
    incidenceData(CC)
    
  })
  
  output$plot1 <- renderPlot({
    
    #Based on the data and analysis type, return the appropriate plot
    plotSwitch(input$ANL, selectedData())
    
  })
  
}

#Make it a shiny app
shinyApp(ui = htmlTemplate("www/index.html"), server = server)


