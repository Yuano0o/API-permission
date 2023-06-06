# Android API-permission mapping methods

- Not comprehensive, but covers **state-of-the-art** methods
	- [12 PScout] \[1]
	- [16 Axplorer] \[2]
	- [18 ARCADE] \[4]
- Includes some related or interesting topics
	- Annotation & Documentary + NLP [6]
	- API-DP(dangerous permission) [9]
	- etc

## Method, Code and Dataset

- [12 PScout] \[1]
	- state-of-the-art 
	- [Code & Dataset](https://security.csl.toronto.edu/pscout/): API level 14-22 (Android 4.11-5.11)
- [16 Axplorer] \[2]
	- state-of-the-art
	- [Dataset](https://github.com/reddr/axplorer): API level 16-25 
- [18 ARCADE] \[4]
	- state-of-the-art
	- [Dataset](https://arcade-android.github.io/arcade/): API level 23-25
- [19 PerRec] \[5]
	- Code & Dataset
- [21 NATIDROID] \[8]
	- native library
	- [Code & Dataset](https://natidroid.github.io/): API level 24-27+29
- [21 PSGen] \[7] 
	- permission specification
	- [Code & Dataset](https://github.com/moonZHH/PSGen): Android 9.0, 10.0, and 11.0
- [22 APMiner] \[9]
	- API-DP
	- [Code & Dataset](https://github.com/ARP-issues/ARP-DP): API level 23-30

# Literature Notes

- [12 PScout] \[1] 
	- Still be used in 2022

- [16 Axplorer] \[2]  
	- **More precise** for the application framework API and that calls the validity of some **prior results**([7 PScout] \[1]) into question  

 - [18 ARCADE] \[4]
	 - Prominent efforts 
		  - [Stowaway], PScout [1], **Axplorer** [2]
	- Dynamic & static approaches 
		 - dynamic approaches > **incomplete** mappings 
		 - static approaches > limitations
			 - lack of path-sensitive analysis > not necessarily correct and may lead to **inaccurate** mappings 
				 - e.g., PScout and Axplorer ([1, 2])
	- Comparison
		- **Compared** with **Axplorer** (considered to be **best performing**)
			- detect on average 43% more unneeded permissions and reduce false alarms in detecting component hijacking by 11 components on average (per image). 
			- Axplorer’s map states that the API requires all these permissions, which is **imprecise** 
	- [6.1.2 API Protection Mapping Breakdown] 

- [20 Semantic-aware Comment Analysis Approach for API Permission Mapping on Android]  \[6]
	- Extract all **comments** and **java documents** from raw Android source code and extract **permission** information using natural language processing(**NLP**) techniques 
	- **Problems** in java document 
		- not complete  
		- natural, unstructured format 
	- Experiment on Android 10, mapped 3,012 APIs with permission 
	- [2.1 Imprecise of Current API Permission Map] 
		- Axplorer [2]
			- coverage: lots of developer-usable APIs, which will actually in APK’s codes, were not mapped on their map 
		- ARCADE [4]
			- one of the state-of-art
			- doesn’t provide full list (only focused on function detection) 
		- PScout [1]
			- number of API found is huge compare to other works 
			- too outdated (extended until 5.1.1) 
		- java document provides detailed information, but previous works Axplorer, ARCADE([2, 4]) doesn’t contain those APIs 

- [21 NATIDROID] \[8]
	- This work analyzed the protection mapping in the **native library** (i.e., code written in C and C++) 
	- Against two **state-of-the-art** tools: AXPLORER [2] and ARCADE [4] 
		- identify up to 464 new API-permission mappings 

- [21 PSGen]]  \[7]
	- PSGen **statically** analyzes the implementation of Android framework and Android kernel to correlate native framework **APIs** with their required **permissions** 
	- Applying: **Android 9.0, 10.0, and 11.0** 
		 - PSGen can **precisely** build the permission specification

- [22 APMiner] \[9] 
	- The study needs the **latest and precise** API-permission mappings 
		- It extracted API-DP mappings from the source code and docs
			- [APR-Issues (arp-issues.github.io)](https://arp-issues.github.io/)
			- https://github.com/ARP-issues/APMINER 
			- https://github.com/ARP-issues/ARP-DP 
		- Inferring API-Permission Mappings (Problems)
			- imprecise or incomplete
			- AXPLORER [2] 
				- more **precise** than PSCOUT [1]
				- contained **few** mappings for **dangerous** permissions 
			- **outdated** datasets 
			- **unavailable** or **inapplicable** tools 

---

- [18 Method-Level Permission Analysis Based on Static Call Graph of Android Apps] \[3]
	- Two major challenges
		- (1) **mapping** permission to APIs; 
		- (2) handling the thousands of methods and method invocations.
	- This mapping of permission and Android API is not provided by Google. There are research works on recovering the mapping information by exploring Android framework distributions. 
		- **PScout** [1] provides an effective way to achieve the mapping information, and its results are used by the method-level permission analysis presented in this paper.

- [19 PerRec] \[5]
	- [Stowaway], [PScout], [Androguard], [Axplorer] 
		- For example, there are four permissions that are checked in native C/C++ code in Android 4.0, but PScout can not handle them automatically
		- In the permission map extracted by Axplorer, we can not find any mapping which contains API android.media.AudioRecord or permission RECORD_AUDIO.
		- Describe a new automatic and more accurate approach

# Reference list

[1]  K. W. Y. Au, Y. F. Zhou, Z. Huang, and D. Lie, ‘PScout: Analyzing the android permission specification’, in _Proceedings of the 2012 ACM conference on computer and communications security_, in CCS ’12. New York, NY, USA: Association for Computing Machinery, 2012, pp. 217–228. doi: [10.1145/2382196.2382222](https://doi.org/10.1145/2382196.2382222).

[2]  M. Backes, S. Bugiel, E. Derr, P. D. McDaniel, D. Octeau, and S. Weisgerber, ‘On demystifying the android application framework: Re-visiting android permission specification analysis’, in _25th USENIX security symposium, USENIX security 16, austin, TX, USA, august 10-12, 2016_, T. Holz and S. Savage, Eds., USENIX Association, 2016, pp. 1101–1118. [Online]. Available: [https://www.usenix.org/conference/usenixsecurity16/technical-sessions/presentation/backes_android](https://www.usenix.org/conference/usenixsecurity16/technical-sessions/presentation/backes_android)

[3]  Y. Hu, W. Kong, D. Ding, and J. Yan, ‘Method-Level Permission Analysis Based on Static Call Graph of Android Apps’, in _2018 5th International Conference on Dependable Systems and Their Applications (DSA)_, Dalian, China: IEEE, Sep. 2018, pp. 8–14. doi: [10.1109/DSA.2018.00014](https://doi.org/10.1109/DSA.2018.00014).

[4]  Y. Aafer, G. Tao, J. Huang, X. Zhang, and N. Li, ‘Precise Android API Protection Mapping Derivation and Reasoning’, in _Proceedings of the 2018 ACM SIGSAC Conference on Computer and Communications Security_, Toronto Canada: ACM, Oct. 2018, pp. 1151–1164. doi: [10.1145/3243734.3243842](https://doi.org/10.1145/3243734.3243842).

[5]  Z. Liu, X. Xia, D. Lo, and J. Grundy, ‘Automatic, highly accurate app permission recommendation’, _Autom Softw Eng_, vol. 26, no. 2, pp. 241–274, Jun. 2019, doi: [10.1007/s10515-019-00254-6](https://doi.org/10.1007/s10515-019-00254-6).

[6]  H. Shim and S. Jung, ‘Semantic-aware Comment Analysis Approach for API Permission Mapping on Android’, in _Proceedings of the 4th International Conference on Natural Language Processing and Information Retrieval_, Seoul Republic of Korea: ACM, Dec. 2020, pp. 61–69. doi: [10.1145/3443279.3443312](https://doi.org/10.1145/3443279.3443312).

[7]  H. Zhou _et al._, ‘Finding the missing piece: Permission specification analysis for android NDK’, in _2021 36th IEEE/ACM international conference on automated software engineering (ASE)_, 2021, pp. 505–516. doi: [10.1109/ASE51524.2021.9678843](https://doi.org/10.1109/ASE51524.2021.9678843).

[8]  C. Li _et al._, ‘NatiDroid: Cross-Language Android Permission Specification’. arXiv, Nov. 15, 2021. Accessed: Jun. 03, 2023. [Online]. Available: [http://arxiv.org/abs/2111.08217](http://arxiv.org/abs/2111.08217)

[9]  Y. Wang _et al._, ‘Runtime Permission Issues in Android Apps: Taxonomy, Practices, and Ways Forward’, _IIEEE Trans. Software Eng._, vol. 49, no. 1, pp. 185–210, Jan. 2023, doi: [10.1109/TSE.2022.3148258](https://doi.org/10.1109/TSE.2022.3148258).
