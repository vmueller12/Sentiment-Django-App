from django.views import generic
from .sentiment import Sentiment
from .forms import TextFieldForm
from .models import InputText, SentAnalysis, MachineLearning
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import CreateView

from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse


from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .sentiment import Sentiment, TopWordsRetriever
from .algorithm import PosNegCounter, MachineLearningClass



    
class SentimentDelete(DeleteView):
    model = InputText
    
    def get_success_url(self):
        return reverse('sent_list')
    
    
class SentimentUpdate(UpdateView):
    model = InputText
    form_class = TextFieldForm
    template_name = "sentiment/index.html"
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        try:
            # if this characters are in title remove
           self.object.title = self.object.title.replace(u"\u2018", "'").replace(u"\u2019", "'")
        except:
            pass
        try:
            self.object.slug = slugify(self.object.title)
        except:
            pass
        self.object.save()
        # create a instance for Sentiment()
        try:
            sent = SentAnalysis()
            ins = Sentiment(self.object.content)
            sent.inputText = self.object
            sent.totalWords =  int(ins.totalWords())
            sent.totalSentences = int(ins.totalSentences())
            topFive = ins.topFiveWords()
            topCleaned = ins.topFiveWordsCleaned()
            topWords = ",".join("(%s,%s)" % tup for tup in topFive)
            topWCleaned = ",".join("(%s,%s)" % tup for tup in topCleaned)
            sent.topFiveWordsCleaned = topWCleaned
            sent.topWords = topWords
            sent.stopWords = int(ins.stopwordsCounter())
            sent.slug = self.object.slug
            sent.ratioTotalStopwords = float(ins.ratioTotalWordStopWord())
            sent.avWordsSentence = float(ins.avWordsPerSentence())
            sent.save()
        except:
            pass
            
        
        try:
            #assign new instance to the model
            ml = MachineLearning()
            ml.inputText = self.object
            ml.slug = self.object.slug
            # creating instance for the MachineLearningClass and PosNegCounter Class
            mlClass = MachineLearningClass(self.object.content)
            pnCounter = PosNegCounter(self.object.content)
            
    
            ml.positiveWords = pnCounter.positiveWords()
            ml.negativeWords = pnCounter.negativeWords()
            ml.swearingWords = pnCounter.swearingWords()
            ml.positiveCounter, ml.negativeCounter = pnCounter.posNegCounter()
            ml.swearingCounter = pnCounter.swearingCount()
            ml.ratioTotalWordsPositive, ml.ratioTotalWordsNegative = pnCounter.ratioTotalWordsPosNeg()

            ml.naiveBayes = mlClass.mlAnalyser()[0]
            ml.mnb = mlClass.mlAnalyser()[1]
            ml.bernoulliNB = mlClass.mlAnalyser()[2]
            ml.confidence = mlClass.outputClassifier()[0]
            ml.totalCategory = mlClass.outputClassifier()[1]
            ml.save()
        except:
            pass
            
        return super(SentimentUpdate, self).form_valid(form)


class SentimentCreate(CreateView):
    form_class = TextFieldForm
    template_name = "sentiment/index.html"

    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        try:
            # if this characters are in title remove
           self.object.title = self.object.title.replace(u"\u2018", "'").replace(u"\u2019", "'")
        except:
            pass
        try:
            self.object.slug = slugify(self.object.title)
        except:
            pass
        self.object.save()
        try:
            sent = SentAnalysis()
            ins = Sentiment(self.object.content)
            sent.inputText = self.object
            sent.totalWords =  int(ins.totalWords())
            sent.totalSentences = int(ins.totalSentences())
            topFive = ins.topFiveWords()
            topCleaned = ins.topFiveWordsCleaned()
            topWords = ",".join("(%s,%s)" % tup for tup in topFive)
            topWCleaned = ",".join("(%s,%s)" % tup for tup in topCleaned)
            sent.topFiveWordsCleaned = topWCleaned
            sent.topWords = topWords
            sent.stopWords = int(ins.stopwordsCounter())
            sent.slug = self.object.slug
            sent.ratioTotalStopwords = float(ins.ratioTotalWordStopWord())
            sent.avWordsSentence = float(ins.avWordsPerSentence())
            sent.save()
            
            
        except:
            pass
        
        try:
            #assign new instance to the model
            ml = MachineLearning()
            ml.inputText = self.object
            ml.slug = self.object.slug
            # creating instance for the MachineLearningClass and PosNegCounter Class
            mlClass = MachineLearningClass(self.object.content)
            pnCounter = PosNegCounter(self.object.content)
            
    
            ml.positiveWords = pnCounter.positiveWords()
            ml.negativeWords = pnCounter.negativeWords()
            ml.swearingWords = pnCounter.swearingWords()
            ml.positiveCounter, ml.negativeCounter = pnCounter.posNegCounter()
            ml.swearingCounter = pnCounter.swearingCount()
            ml.ratioTotalWordsPositive, ml.ratioTotalWordsNegative = pnCounter.ratioTotalWordsPosNeg()

            ml.naiveBayes = mlClass.mlAnalyser()[0]
            ml.mnb = mlClass.mlAnalyser()[1]
            ml.bernoulliNB = mlClass.mlAnalyser()[2]
            ml.confidence = mlClass.outputClassifier()[0]
            ml.totalCategory = mlClass.outputClassifier()[1]
            ml.save()
        except:
            pass
        
            
        return super(SentimentCreate, self).form_valid(form)


    
class SentimentDetail(DetailView):
    template_name = 'sentiment/detail.html'
    model = InputText
    
    
    def get_context_data(self, **kwargs):
       
       
        context = super(SentimentDetail, self).get_context_data(**kwargs)
        try:
            try:
                qrsAnalysis = SentAnalysis.objects.get(slug=self.object.slug)
            except:
                pass
            try:
                qrsMachineLearning = MachineLearning.objects.get(slug=self.object.slug)
            except:
                pass
            topW = TopWordsRetriever(qrsAnalysis.topWords)
            words, num = topW.topWords()
            context['stopWords'] = qrsAnalysis.stopWords
            context['totalWords'] = qrsAnalysis.totalWords
            context['averageWPS'] = int(qrsAnalysis.avWordsSentence)
            context['totalSentences'] = qrsAnalysis.totalSentences
            context['ratioWS'] = int(qrsAnalysis.ratioTotalStopwords)
            context['word1'] = words[0]
            context['word2'] = words[1]
            context['word3'] = words[2]
            context['word4'] = words[3]
            context['word5'] = words[4]
            context['num1'] = num[0]
            context['num2'] = num[1]
            context['num3'] = num[2]
            context['num4'] = num[3]
            context['num5'] = num[4]
            
            topCL = TopWordsRetriever(qrsAnalysis.topFiveWordsCleaned)
            wC, nC = topCL.topWords()
            
            
            
            
            context['wC1'] = wC[0]
            context['wC2'] = wC[1]
            context['wC3'] = wC[2]
            context['wC4'] = wC[3]
            context['wC5'] = wC[4]
            context['nC1'] = nC[0]
            context['nC2'] = nC[1]
            context['nC3'] = nC[2]
            context['nC4'] = nC[3]
            context['nC5'] = nC[4]
            
            context['swearingList'] = topCL.wordProcessing(qrsMachineLearning.swearingWords)
            context['positiveList'] = topCL.wordProcessing(qrsMachineLearning.positiveWords)
            context['negativeList'] = topCL.wordProcessing(qrsMachineLearning.negativeWords)
            context['naive'] = qrsMachineLearning.naiveBayes
            context['mnb'] = qrsMachineLearning.mnb
            context['bernoulli'] = qrsMachineLearning.bernoulliNB
            context['totalCat'] = qrsMachineLearning.totalCategory
            context['confidence'] =qrsMachineLearning.confidence
            
            context['poCo'] = qrsMachineLearning.positiveCounter
            context['neCo'] = qrsMachineLearning.negativeCounter
            context['swCo'] = qrsMachineLearning.swearingCounter
            context['rtwp'] = qrsMachineLearning.ratioTotalWordsPositive
            context['rtwn'] = qrsMachineLearning.ratioTotalWordsNegative
            
        except:
            pass
        
        return context
    
    
    
    
class SentimentList(ListView):
    template_name = 'sentiment/list.html'
    model = InputText
    
    def get_queryset(self, *args, **kwargs):
        qs = super(SentimentList, self).get_queryset(*args, **kwargs).order_by("-created")
        return qs