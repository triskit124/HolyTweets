

class HolyBot:
    """
    Holy Bot implementation
    """

    def __init__(self, corpusFile=None):
        self.uniqueWords = set()        # Set of unique words pulled from processed corpus
        self.loadCorpus(corpusFile)     # Loads and processes the corpus file

    def loadCorpus(self, corpusFile: str):
        """
        Loads in a bible to use as a corpus of words. Will convert from .xml to .txt format if possible.
        Fills the Set self.uniqueWords after processing the corpus.

        :param corpusFile: [string] representing which corpus file to load, without the extension (ex: 'English')
        """
        import os

        # Look for .txt file first
        if not os.path.exists(corpusFile + '.txt'):
            # Look for .xml file
            if os.path.exists(corpusFile + '.xml'):
                # If .xml file exists, convert to .txt
                print('Converting corpus file {} to txt format'.format(corpusFile))
                self.convertXmlToTxt(corpusFile)
            else:
                raise 'Cannot find corpus file specified'

        # Open and process .txt file
        with open(corpusFile + '.txt') as f:
            lines = f.readlines()
            for line in lines:
                # extract words from processed line of text
                newWords = self.processString(line).split(' ')

                # union new words into the unique words Set
                self.uniqueWords.update(newWords)
            print('Done processing corpus, found {} unique words'.format(len(self.uniqueWords)))

    def convertXmlToTxt(self, corpusFile: str):
        """
        Helper function to convert from .xml format to .txt format.

        :param corpusFile: [string] representing which corpus file to load, without the extension (ex: 'English')
        """
        from xml.etree.ElementTree import fromstring
        root = fromstring(open(corpusFile + '.xml').read())
        with open(corpusFile + '.txt', 'w', encoding='utf-8') as out:
            for n in root.iter('seg'):
                out.write(n.text.strip() + '\n')

    def processString(self, s: str) -> str:
        """
        Helper function to process strings (convert all to lowercase, remove unwanted chars, etc.)

        :param s: string of text to process
        :return: processed string of text
        """
        # I don't like using regex so here we are with this jank
        return s \
            .replace('\n', '') \
            .replace('\t', '') \
            .replace('.', '') \
            .replace(',', '') \
            .replace(';', '') \
            .replace('(', '') \
            .replace(')', '') \
            .replace(':', '') \
            .replace('!', '') \
            .replace('?', '') \
            .lower()

    def tweet(self, numTweets=1):
        """
        Looks through Twitter to find a Tweet to reply to, and Tweets it.

        :param numTweets: [uint] number of tweets to send
        """

        # TODO: scrape tweet here using API


        tweet = '\tA full circle moment 😳 Ime Udoka goes from playing against Curry to coaching against him in the NBA Finals.'
        print('\n\n')
        print(tweet)

        # process the tweet
        tweet = self.processString(tweet)
        words = tweet.split(' ')

        # Determine number of words that are in the Bible
        wordsInBible = sum([1 if word in self.uniqueWords else 0 for word in words])
        percentInBible = 100 * wordsInBible / len(words)

        if percentInBible < 30:
            print('\tOnly {:.1f}% of these words are in the Bible. Find God.'.format(percentInBible))
        elif percentInBible < 60:
            print('\t{:.1f}% of these words are in the Bible. '.format(percentInBible))
        else:
            print('\t{:.1f}% of these words are in the Bible. Based.'.format(percentInBible))

        # debug
        print('\n')
        for word in words:
            if word in self.uniqueWords:
                print(word, 'is in bible')
            else:
                print(word, 'not in bible')


if __name__ == '__main__':
    holyBot = HolyBot(corpusFile='English')
    holyBot.tweet()
