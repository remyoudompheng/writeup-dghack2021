package main

import (
	"encoding/json"
	"fmt"
	"math/rand"
	"os"
)

const GLOUTON = false

func main() {
	var s State
	for i := range s.classe {
		s.classe[i] = uint32(i % 3)
	}
	s.score = s.compute()
	println(s.score)

	// Un recuit simulé.
	i, j := 0, 0
	temp := 0
	for k := 0; k < 1e6; k++ {
		// i = k % 90
		// j = k % 89
		i++
		j++
		if i == 90 {
			i = 0
		}
		if j == 89 {
			j = 0
		}
		if i == 0 && j == 0 {
			temp++
		}
		// a, b pair of indices
		a, b := i, j
		if j >= i {
			b++
		}
		n := s.score
		s.swap(a, b)
		s.score = s.compute()
		n2 := s.score
		if n2 >= n {
			// ok
			if n2 > n {
				fmt.Println("new score", n2)
				if n2 > 3000 {
					fmt.Println("itération", k)
					break
				}
			}
		} else {
			// go down with probability P = exp(temp/10*(n-n2)), k => infty
			f := rand.ExpFloat64()
			if !GLOUTON && 10*f > float64(temp)*float64(n-n2) {
				// keep
				fmt.Println("down", n2-n, "temp =", temp, f)
			} else {
				s.swap(a, b)
				s.score = n
			}
		}
	}

	var classes [3][]int
	for i, c := range s.classe {
		classes[c] = append(classes[c], i+1)
	}
	json.NewEncoder(os.Stdout).Encode(classes)

	// % python score.py -i dghack2021-ecole-repartition.json -c z.json
	// score total : 3050
}

type State struct {
	classe [90]uint32
	score  int
}

func (s *State) compute() int {
	res := 0
	for i, friends := range ELEVES {
		for r, j := range friends {
			if s.classe[i] == s.classe[j-1] {
				res += 20 - 5*r
			}
		}
	}
	return res
}

func (s *State) swap(i, j int) {
	if s.classe[i] == s.classe[j] {
		return
	}
	s.classe[i], s.classe[j] = s.classe[j], s.classe[i]
}

var ELEVES = [...][4]uint32{
	// jq -c -S '.[] | .friends' dghack2021-ecole-repartition.json
	// | sed -r 's+\[(.*)\]+{\1},+'
	{89, 45, 27, 59},
	{77, 84, 67, 23},
	{72, 81, 31, 75},
	{16, 54, 25, 85},
	{25, 86, 49, 24},
	{17, 76, 82, 49},
	{68, 3, 76, 29},
	{36, 60, 14, 43},
	{46, 54, 36, 62},
	{2, 27, 11, 29},
	{42, 45, 65, 9},
	{70, 60, 18, 64},
	{24, 83, 76, 3},
	{29, 53, 17, 42},
	{79, 82, 90, 3},
	{64, 73, 36, 39},
	{37, 46, 15, 36},
	{58, 25, 43, 39},
	{79, 52, 13, 30},
	{53, 67, 43, 33},
	{46, 67, 61, 31},
	{4, 53, 67, 59},
	{90, 49, 20, 76},
	{42, 63, 6, 43},
	{75, 37, 61, 70},
	{47, 61, 23, 28},
	{34, 87, 88, 40},
	{61, 43, 14, 52},
	{38, 53, 32, 68},
	{46, 9, 81, 79},
	{67, 82, 53, 17},
	{23, 50, 76, 67},
	{22, 64, 88, 50},
	{60, 20, 44, 65},
	{59, 80, 63, 36},
	{22, 39, 58, 81},
	{7, 62, 23, 38},
	{77, 32, 17, 61},
	{7, 74, 26, 25},
	{62, 76, 89, 82},
	{66, 29, 89, 74},
	{24, 77, 28, 18},
	{71, 7, 19, 48},
	{40, 75, 76, 77},
	{56, 21, 65, 18},
	{63, 22, 71, 38},
	{25, 56, 4, 9},
	{35, 34, 76, 58},
	{27, 32, 59, 61},
	{71, 70, 26, 87},
	{52, 80, 82, 44},
	{77, 15, 84, 42},
	{38, 70, 44, 10},
	{16, 4, 44, 69},
	{57, 71, 44, 17},
	{35, 27, 45, 61},
	{15, 17, 88, 45},
	{1, 18, 35, 43},
	{63, 47, 8, 42},
	{84, 54, 46, 35},
	{11, 70, 83, 10},
	{12, 25, 51, 44},
	{77, 50, 75, 2},
	{87, 54, 77, 9},
	{18, 90, 69, 34},
	{20, 87, 1, 8},
	{32, 66, 5, 16},
	{31, 45, 52, 13},
	{89, 25, 3, 49},
	{80, 64, 16, 35},
	{46, 86, 51, 61},
	{55, 21, 86, 13},
	{87, 60, 34, 47},
	{88, 11, 61, 62},
	{27, 21, 1, 3},
	{89, 35, 9, 31},
	{22, 45, 51, 86},
	{31, 36, 52, 63},
	{39, 71, 51, 33},
	{83, 67, 76, 90},
	{90, 9, 72, 7},
	{43, 49, 66, 10},
	{8, 19, 36, 72},
	{14, 38, 59, 82},
	{62, 11, 17, 15},
	{23, 25, 30, 55},
	{29, 24, 40, 20},
	{13, 64, 87, 1},
	{45, 6, 82, 40},
	{60, 30, 29, 5},
}
