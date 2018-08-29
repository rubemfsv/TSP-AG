# TSP-AG

## Aplicação de algoritmo genético de Holland ao problema do caixeiro viajante

Imagine que você é um vendedor e recebeu um mapa. Nele, você vê que o mapa contém um total de 20 cidades e lhe dizem que é seu trabalho visitar cada uma dessas cidades para fazer uma venda.

Antes de viajar, você provavelmente desejará planejar uma rota para minimizar seu tempo de viagem. Felizmente, podemos facilmente encontrar uma rota razoavelmente boa sem precisar fazer muito mais do que olhar para o mapa. No entanto, quando encontramos uma rota que acreditamos ser ideal, como podemos testar se essa é realmente a rota ideal?

Não podemos na prática, porém, podemos na teoria.

Para entender por que é tão difícil provar a rota ideal, vamos considerar um mapa semelhante com apenas 3 cidades no lugar das 20. Para encontrar uma única rota, primeiro precisamos escolher uma localização inicial a partir das três cidades possíveis no mapa. Em seguida, teríamos uma escolha de duas cidades para o segundo local e, finalmente, há apenas uma cidade para escolher para completar nossa rota. Isso significaria que há 3 x 2 x 1 rotas diferentes para escolher no total.

Isso significa que, para este exemplo, existem apenas 6 rotas diferentes para escolher. Portanto, para este caso de apenas 3 locais, é razoavelmente trivial calcular cada uma dessas 6 rotas e encontrar a mais curta. O número de rotas possíveis é um fatorial do número de locais a serem visitados, e o problema com os fatoriais é que eles crescem em tamanho notavelmente rápido.

Por exemplo, o fatorial de 10 é 3628800, mas o fatorial de 20 é um gigantesco, 2432902008176640000.

Então, se quisermos encontrar o caminho mais curto para o nosso mapa de 20 cidades, teríamos que avaliar 2432902008176640000 rotas diferentes. Mesmo com o poder da computação moderna, isso é terrivelmente impraticável e, para problemas ainda maiores, é quase impossível.

Mapa:
http://www.theprojectspot.com/images/post-assets/map1.jpg

## Procurando uma solução

Embora possa não ser prático encontrar a melhor solução para um problema como o nosso, temos algoritmos que nos permitem descobrir soluções próximas, como o algoritmo do vizinho mais próximo e a otimização de enxames. Esses algoritmos são capazes de encontrar uma solução "boa o suficiente" para o problema do vendedor ambulante surpreendentemente rápido. 

Uma solução válida precisaria representar uma rota em que cada cidade é incluída pelo menos uma vez e apenas uma vez. Se uma rota contivesse uma única localização mais de uma vez, ou perdesse completamente uma localização, não seria válida e teríamos um valioso tempo de cálculo calculando sua distância.

Para garantir que o algoritmo genético realmente atenda a esse requisito, são necessários tipos especiais de mutação e métodos de cruzamento.

Em primeiro lugar, o método de mutação só deve ser capaz de embaralhar a rota, nunca deve adicionar ou remover um local da rota, caso contrário, arriscaria criar uma solução inválida. 

Agora lidamos com o método de mutação, precisamos escolher um método de crossover que possa impor a mesma restrição.

Um método de crossover capaz de produzir uma rota válida é o crossover ordenado. Nesse método de cruzamento, selecionamos um subconjunto do primeiro pai e, em seguida, adicionamos esse subconjunto à descendência. Quaisquer valores ausentes são adicionados aos descendentes do segundo pai para que sejam encontrados.


## Criando o Algoritmo Genético

Para começar, criamos uma classe que possa codificar as cidades.

Depois, criamos uma classe que contém todas as nossas cidades de destino para a nossa viagem.

Em seguida, precisamos de uma classe que possa codificar nossas rotas. Geralmente, elas são chamadas de viagens.

Nós também precisamos criar uma classe que possa conter uma população de viagens das cidades candidatas.

Em seguida, vamos criar uma classe GA que manipule o funcionamento do algoritmo genético e desenvolva nossa população de soluções.

Agora podemos criar nosso método principal, adicionar nossas cidades e desenvolver uma rota para nosso problema do caixeiro viajante.


## Saída:

Distancia inicial: 1996
Distancia final: 940
Solução:
|60, 200|20, 160|40, 120|60, 80|20, 40|20, 20|60, 20|100, 40|160, 20|200, 40|180, 60|120, 80|140, 140|180, 100|200, 160|180, 200|140, 180|100, 120|100, 160|80, 180|


Após 100 gerações, conseguimos encontrar uma rota duas vezes melhor do que a nossa original e, provavelmente, bem perto do ideal.

http://www.theprojectspot.com/images/post-assets/map2.jpg
