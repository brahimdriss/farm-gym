from gym.spaces.space import Space
import numpy as np


class Union(Space):
    """
    A tuple (i.e., product) of simpler spaces

    Example usage:
    self.observation_space = spaces.Tuple((spaces.Discrete(2), spaces.Discrete(3)))
    """

    def __init__(self, spaces):
        self.spaces = spaces
        for space in spaces:
            assert isinstance(space, Space), "Elements of the tuple must be instances of gym.Space"
        super(Union, self).__init__(None, None)

    def seed(self, seed=None):
        [space.seed(seed) for space in self.spaces]

    def sample(self):
        n = np.random.randint(len(self.spaces))
        return n, self.spaces[n].sample()

    def contains(self, x):
        return any(space.contains(x) for space in self.spaces)

    def __repr__(self):
        return "Union(" + ", ".join([str(s) for s in self.spaces]) + ")"

    def to_jsonable(self, sample_n):
        # serialize as list-repr of union of vectors
        return []
        # return [space.to_jsonable([sample[i] for sample in sample_n]) \                for i, space in enumerate(self.spaces)]

    def from_jsonable(self, sample_n):
        return []
        # return [sample for sample in zip(*[space.from_jsonable(sample_n[i]) for i, space in enumerate(self.spaces)])]

    def __getitem__(self, index):
        return self.spaces[index]

    def __len__(self):
        return len(self.spaces)

    def __eq__(self, other):
        return isinstance(other, Union) and self.spaces == other.spaces


class MultiUnion(Space):
    """
    A tuple (i.e., product) of simpler spaces

    Example usage:
    self.observation_space = spaces.Tuple((spaces.Discrete(2), spaces.Discrete(3)))
    """

    def __init__(self, spaces, maxnonzero=np.infty):
        self.spaces = spaces
        self.maxnonzero = maxnonzero
        for space in spaces:
            assert isinstance(space, Space), "Elements of the tuple must be instances of gym.Space"
        super(MultiUnion, self).__init__(None, None)

    def seed(self, seed=None):
        [space.seed(seed) for space in self.spaces]

    def sample(self): # Sampling without replacement (not twice in the same space).
        m = np.random.randint(min(self.maxnonzero + 1, len(self.spaces)+1))
        indexes = list(range(len(self.spaces)))
        sampled_indexes = []
        for j in range(m):
            n = np.random.choice(indexes)
            indexes.remove(n)
            sampled_indexes.append(n)
        samples = []
        for n in sampled_indexes:
            if (len(self.spaces)==1):
                samples.append(self.spaces[n].sample())
            else:
                samples.append((n, self.spaces[n].sample()))
        #print("sample",m,sampled_indexes,samples)
        return samples

    def contains(self, x):
        if len(x) > self.maxnonzero:
            return False
        # print("SPACES",self.spaces)
        # print("X",x)
        for xx in x:
            contains = []
            for space in self.spaces:
                # print("xx",xx,"space",space)
                try:
                    if space.contains(xx):
                        contains.append(True)
                        break
                except:
                    pass
            if contains == []:
                return False
            # if not any(space.contains(xx) for space in self.spaces):
            #    return False
        return True

    def __repr__(self):
        s = "MultiUnion" + (("[" + str(self.maxnonzero) + "]") if self.maxnonzero < np.infty else "")
        return s + "(" + ", ".join([str(s) for s in self.spaces]) + ")"

    def to_jsonable(self, sample_n):
        # serialize as list-repr of union of vectors
        return []
        # return [space.to_jsonable([sample[i] for sample in sample_n]) \                for i, space in enumerate(self.spaces)]

    def from_jsonable(self, sample_n):
        return []
        # return [sample for sample in zip(*[space.from_jsonable(sample_n[i]) for i, space in enumerate(self.spaces)])]

    def __getitem__(self, index):
        return self.spaces[index]

    def __len__(self):
        return len(self.spaces)

    def __eq__(self, other):
        return isinstance(other, MultiUnion) and self.spaces == other.spaces


class Sequence(Space):

    def __init__(self, space, maxnonzero=np.infty):
        self.space = space
        self.maxnonzero = maxnonzero
        assert isinstance(space, Space), "Elements of the tuple must be instances of gym.Space"
        super(Sequence, self).__init__(None, None)

    def seed(self, seed=None):
        self.space.seed(seed)

    def sample(self): # Sampling with replacement
        m = np.random.randint(self.maxnonzero + 1)
        samples = []
        for n in range(m):
                samples.append(self.space.sample())
        return samples

    def contains(self, x):
        if len(x) > self.maxnonzero:
            return False
        for xx in x:
            if not self.space.contains(xx):
                return False
        return True

    def __repr__(self):
        s = "Sequence" + (("[" + str(self.maxnonzero) + "]") if self.maxnonzero < np.infty else "")
        return s + "(" + str(self.space) + ")"

    def to_jsonable(self, sample_n):
        # serialize as list-repr of union of vectors
        return []
        # return [space.to_jsonable([sample[i] for sample in sample_n]) \                for i, space in enumerate(self.spaces)]

    def from_jsonable(self, sample_n):
        return []
        # return [sample for sample in zip(*[space.from_jsonable(sample_n[i]) for i, space in enumerate(self.spaces)])]

    def __len__(self):
        return len(self.space)**self.maxnonzero if self.maxnonzero < np.infty else np.infty

    def __eq__(self, other):
        return isinstance(other, Sequence) and self.space == other.space
